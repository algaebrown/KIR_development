#https://www.vscentrum.be/cluster-doc/software/r-cla-in-scripts

args <- commandArgs(TRUE)

print(length(args))

sample_location <- as.character(args[1]) # "/nrnb/users/ramarty/kir/TCGA/exomes/943e35da-f8f6-4991-8511-ad6bf962a66b/"
fastq_pattern_1 <- as.character(args[2]) # '_1.fastq' <- removed .fastq to make a valid regular expression?
fastq_pattern_2 <- as.character(args[3]) # '_2.fastq'
results_directory <- as.character(args[4]) #
bowtie_threads <- as.double(args[5]) # 1

source("PING_extractor_v1.0.R")

ping_extractor(sample.location = sample_location,
                 fastq.pattern.1 = fastq_pattern_1,
                 fastq.pattern.2 = fastq_pattern_2,
                 results.directory = results_directory,
                 bowtie.threads = bowtie_threads)

