import os
import sys
import time
import random
import ahocorasick # need
import pandas as pd
from Bio import SeqIO
from itertools import izip_longest
import pathos.multiprocessing as mp # need


def main(input_fastq, output_dir, kmer_ref, name):
    '''
    takes fastq and get the k-mer count
    input_fastq: stripped and remapped to KIR .bam file converted to fastq (/nrnb/users/ramarty/TCGA/exome/{barcode}/KIR_and_unmapped.aligned.fastq
    output_dir: $out/features: one barcode one k-mer file; two files in the features folder: _counts.txt, _read_counts.txt
    - _counts.txt
    - _read_counts.txt
    kmer_ref: /cellar/users/ramarty/Data/kir/kmers/kmer_groups/kir_four_random.txt
    name: kir_four_random
    '''

    start_time = time.time()

    # Split fastq files
    num_of_threads = 8
    file_splitter = FileSplitter(input_fastq, output_dir, num_of_threads)
    small_output_files = file_splitter.perform_split()

    files_split_time = time.time()
    print "Files split:", str(files_split_time - start_time)

    # Build automan
    kmer_counter = KmerCounter(kmer_ref)

    # Parallelize
    pool = mp.ProcessingPool(num_of_threads)
    results = pool.map(kmer_counter.count_kmers, small_output_files)

    parallelization_time = time.time()
    print "Parallelization time:", str(parallelization_time - files_split_time)

    # Recombine the parallelized results
    combined_counts = list(pd.concat([x[0].transpose() for x in results]).sum())
    combined_counts_reads = list(pd.concat([x[1].transpose() for x in results]).sum())

    # Output results - need both kmer and read specific
    with open('{0}/{1}_counts.txt'.format(output_dir, name), 'w') as out_file:
        for kmer in combined_counts:
            out_file.write('{0}\n'.format(kmer))
    with open('{0}/{1}_read_counts.txt'.format(output_dir, name), 'w') as out_file:
        for kmer in combined_counts_reads:
            out_file.write('{0}\n'.format(kmer))

    # Remove temporary files
    for sof in small_output_files:
        os.remove(sof)


###########################################  Classes  #####################################


class FileSplitter(object):

    def __init__(self, input_fasta, output_dir, threads):
        self.input_fasta = input_fasta
        self.output_dir = output_dir
        self.file_length = self._file_length()
        self.threads = threads
        self.sfl = self._small_file_length()

    def _file_length(self):
        with open(self.input_fasta) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def _small_file_length(self):
        sfl = int(self.file_length) / int(self.threads)
        sfl += 4 - (sfl % 4) # number of lines with fastq read
        return sfl

    # need to put split fastqs in output directory
    def perform_split(self):
        with open(self.input_fasta) as f:
            small_out_files = []
            random.seed(0)
            for i, g in enumerate(grouper(self.sfl, f, fillvalue=''), 1):
                lfn = self.input_fasta.split('/')[-1].split('fastq')[0]
                sof = '{0}/{1}{2}.{3}.fastq'.format(self.output_dir, lfn, str(i), str(random.random())[:5])
                small_out_files.append(sof)
                with open(sof, 'w') as fout:
                    fout.writelines(g)
        return small_out_files


# adjust for naive search when aho isn't installed
class KmerCounter(object):

    def __init__(self, kmer_ref):
        self.kmers = [x.strip() for x in open(kmer_ref).readlines()]
        self.A = self._build_automan()

    def _build_automan(self):
        A = ahocorasick.Automaton() # method to find substring. makes the k-mers into a searching tree to speed up searching
        for index, pattern in enumerate(self.kmers): # for all k-mers we are searching
            A.add_word(pattern, (index, pattern))
        A.make_automaton()
        return A

    def aho_corasick(self, input_fastq):
        '''
        fastq uses aho_corasick to find the k-mer counts. return a dict of keys = k-mer; values = k-mer count.
        '''
        p_mers = [0 for x in self.kmers] # initialize with every k-mer count as 0
        p_mers_reads = [0 for x in self.kmers]
        # speed up assignment to p_mer
        pmer_dict = {}
        for i, mer in enumerate(self.kmers):
            pmer_dict[mer] = i
        # actual search
        fasta_sequences = SeqIO.parse(open(input_fastq),'fastq')
        
        for fasta in fasta_sequences: # iterate through reads
            sequence = fasta.seq.tostring()
            for item in self.A.iter(sequence): # just a way to search all the k-mers (built in A) in `sequence`; returns end_index, (index, k-mer)
                p_mers[pmer_dict[item[1][1]]] += 1 # +1 to that k-mer
            for item in self.A.iter(sequence):
                p_mers_reads[pmer_dict[item[1][1]]] += 1
                break
        return p_mers, p_mers_reads

    def count_kmers(self, input_fastq):
        '''
        putting k-mer counts to the dataframe
        '''
        p_mers, p_mers_reads = self.aho_corasick(input_fastq) # count the k-mer, the _count and _read seems to be the same?
        p_mers = pd.DataFrame(p_mers)
        p_mers.index = self.kmers
        p_mers_reads = pd.DataFrame(p_mers_reads)
        p_mers_reads.index = self.kmers
        return p_mers, p_mers_reads


###########################################  Helper Arguments  #####################################


def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


###########################################  Import Arguments  #####################################

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print "Invalid arguments."
        sys.exit()
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))



'''
Arguments for LICR:

/data/rmarty/exome_samples_trimmed/

samples: CRCp10TIL_AACGTGAT.fastq CRCp3TIL_AAGGACAC.fastq CRCp4TIL_GACAGTGC.fastq CRCp5TIL_ATGCCTAA.fastq CRCp7TIL_GAATCTGA.fastq Lp1PBMC_AAACATCG.fastq Lp2PBMC_GAGTTAGC.fastq Lp3PBMC_CGAACTTA.fastq Lp4PBMC_GATAGACA.fastq

output:
/scratch/cluster/rmarty/KIRcount_output/CRCp10TIL_AACGTGAT

ppft >=1.6.4.5
dill >=0.2.5
pox >=0.2.2
multiprocess >=0.70.4

dill?

'''
