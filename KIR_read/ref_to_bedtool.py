# input: reference genome
# output: tab-delimited txt file with region_name, length

from Bio import SeqIO

def fasta_to_bedtools(ref_fasta, output_path):
    '''
    input: 
    - ref_fasta: reference sequence as fasta file, for example: /cellar/users/ramarty/Data/kir/ref/all_alleles_and_random
    - output_path: folder to contain outputs

    output: three files
    - .bed can feed into bedtools
    - .tsv feed into bedtools genomecov as -g
    - KIR_annotation maps IPD gene ID to KIR allele name and type.
    '''
    # initialize filename
    fname = ref_fasta.split('/')[-1]
    bed_file = output_path + fname + '.bed'
    genomecov_file = output_path + fname + '.tsv'
    KIR_annotation = output_path + 'KIR_annotation' + '.tsv'

    
    # open new output file
    with open(bed_file, 'w') as b:
        with open(genomecov_file, 'w') as g:
            with open(KIR_annotation, 'w') as k:
                k.write('\t'.join(['KIR_ID', 'allele', 'gene']) + '\n')




    # read fasta file
    with open(ref_fasta) as f:
        for record in SeqIO.parse(f, 'fasta'):
            
            # for each record, pull name, calculate length
            name = record.id
            length = str(len(record.seq))

            # which KIR it belongs to
            KIR_allele = record.description.split(' ')[1]
            KIR_gene = KIR_allele.split('*')[0]

            #print(name, length, KIR_allele, KIR_gene)
            

    # write to tsv
            with open(bed_file, 'a') as b:
                with open(genomecov_file, 'a') as g:
                    with open(KIR_annotation, 'a') as k:
                        g.write('\t'.join([name, length])+'\n')
                        b.write('\t'.join([name, '0', length]) + '\n')
                        k.write('\t'.join([name, KIR_allele, KIR_gene]) + '\n')
                        
