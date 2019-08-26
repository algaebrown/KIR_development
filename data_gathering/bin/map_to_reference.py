import time
import sys
import os
import subprocess


# inputs: input fastq file, output bam file, reference
# remap the reads from chr19, random genes and unmapped reads to reference sequence containing all KIR alleles
# argv[1]: fastq from `convert_to_fastq2.py`
# argv[2]: output_mapped_bam file is the remapped to KIR regions .bam in /nrnb/users/ramarty/TCGA/exome/{barcode}/KIR_and_unmapped.aligned.bam
# argv[3]: reference sequence containing all KIR alleles at `/cellar/users/ramarty/Data/kir/ref/all_alleles_and_random cellar`

###########################################  Main Method  #####################################

def main(input_fastq, output_mapped_bam, ref, system):

    # map to reference
    map_to_reference(input_fastq, output_mapped_bam, ref, system)
    print "Mapped to reference."


###########################################  Helper Methods  #####################################


def map_to_reference(input, outdir, ref, system):
    if system == 'cellar':
        # Import tools (this will obviously have to change)
        samtools="/cellar/users/hcarter/programs/samtools-1.2/samtools"
        bowtie2='/cellar/users/ramarty/programs/bowtie2-2.2.9/bowtie2'
        cmd = '{0} -k 1 -x {1} -U {2} ' \
            '| {3} view -bS -h -F 4 - > {4}'.format(bowtie2, ref, input, samtools, outdir)
        os.system(cmd)
    else:
        cmd = 'bowtie2  -x {0} -U {1} ' \
            '| samtools view -bS -h -F 4 - > {2}'.format(ref, input, outdir)
        os.system(cmd)





###########################################  Import Arguments  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 5:
        print "Invalid arguments."
        sys.exit()
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))

# inputs: input fastq file, output bam file, reference

