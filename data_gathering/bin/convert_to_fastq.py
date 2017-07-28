import time
import sys
import os


# inputs: input bam file, output fastq file

###########################################  Main Method  #####################################


def main(input_bam, output_fastq):

    # bam to fastq
    bam_to_fastq(input_bam, output_fastq)
    print "Bam converted to fastq."


###########################################  Helper Methods  #####################################

def bam_to_fastq(f_in, f_out):
    cmd = '{0}/bamToFastq -i {1} -fq {2}'.format(bedtools, f_in, f_out)
    os.system(cmd)


# Import tools (this will obviously have to change)
bedtools="/cellar/users/hcarter/programs/bedtools-2.17.0/bin"


###########################################  Import Arguments  #####################################

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 3:
        print "Invalid arguments."
        sys.exit()
    sys.exit(main(sys.argv[1], sys.argv[2]))


