import time
import sys
import os
import subprocess


# inputs: input fastq file, output bam file, reference

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

