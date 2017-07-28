#https://www.vscentrum.be/cluster-doc/software/r-cla-in-scripts

args <- commandArgs(TRUE)

print(length(args))

sample_location <- as.character(args[1]) # "PING_sequences/" <- for now
results_directory <- as.character(args[2]) # /nrnb/users/ramarty/kir/TCGA/exomes/943e35da-f8f6-4991-8511-ad6bf962a66b/
read_cap <- as.double(args[3])

source("PING_gc_caller_v1.1.R")


ping_gc_caller(make.graphs = FALSE, sample.location = sample_location, results.directory = results_directory, read.cap = read_cap)

'''
ping_gc_caller <- function(
  run.MIRA = TRUE,
  run.KFF = TRUE,
  make.graphs = FALSE,
  sample.location = "PING_sequences/",
  threshold.file = "Resources/gc_resources/defaultThresholds.txt",
  threshold.KFF = 0.2,
  read.cap = 120000,
  results.directory = ""
  )
 '''
