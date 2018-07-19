import time
import sys
import os


# inputs: input bam file, output fastq file

###########################################  Main Method  #####################################

# add in sorted_rmdup_bam if this works...
def main(input_bam, sorted_bam, dedup_bam, output_fastq1, system):

    # sort bam file
    bam_sort(input_bam, sorted_bam, system)
    print "Bam is sorted."

    # dedup bam file

    print "Bam is deduped."
    bam_remove_dup(sorted_bam, dedup_bam, system)

    # bam to fastq
    bam_to_fastq(dedup_bam, output_fastq1, system)
    print "Bam converted to fastq."


###########################################  Helper Methods  #####################################


def bam_to_fastq(f_in, f_out1, system):
    if system == 'cellar':
        # Import tools (this will obviously have to change)
        bedtools="/cellar/users/hcarter/programs/bedtools-2.17.0/bin"
        cmd = '{0}/bamToFastq -i {1}.bam -fq {2}'.format(bedtools, f_in, f_out1)
        os.system(cmd)
    else:
        cmd = 'bamToFastq -i {0}.bam -fq {1} -fq2 {2}'.format(f_in, f_out1)
        os.system(cmd)


def bam_sort(f_in, f_out, system):
    if system == 'cellar':
        # Import tools (this will obviously have to change)
        samtools="/cellar/users/hcarter/programs/samtools-1.2/samtools"
        cmd = '{0} sort -n {1} {2}'.format(samtools, f_in, f_out)
        os.system(cmd)
    else:
        # TODO: need to check this to run it on licr
        cmd = 'samtools sort -n {0} {1}'.format(f_in, f_out)
        os.system(cmd)

def bam_remove_dup(f_in, f_out, system):
    if system == 'cellar':
        # Import tools (this will obviously have to change)
        samtools="/cellar/users/hcarter/programs/samtools-1.1/samtools"
        cmd = '{0} rmdup {1}.bam {2}'.format(samtools, f_in, f_out)
        os.system(cmd)
    else:
        # TODO: need to check this to run it on licr
        cmd = 'samtools sort -n {0} {1}'.format(f_in, f_out)
        os.system(cmd)


###########################################  Import Arguments  #####################################

if __name__ == "__main__":
    start_time = time.time()
    print sys.argv
    if len(sys.argv) != 6:
        print "Invalid arguments."
        sys.exit()
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))


