#! /bin/csh
#$ -V
#$ -S /bin/csh
#$ -o /cellar/users/ramarty/Data/kir/sge-system_files
#$ -e /cellar/users/ramarty/Data/kir/sge-system_files
#$ -cwd
#$ -t 1-29
#$ -l h_vmem=1G
#$ -tc 50
#$ -l long
date
hostname
set lengths=(16 17 18 19 11 12 13 14 15 20 21 22 23 24 29 9 25 10 38 27 37 33 32 46 31 36 34 30 26)

set length=$lengths[$SGE_TASK_ID]

/cellar/users/ramarty/programs/netMHCIIpan-3.1/netMHCIIpan -f /cellar/users/ramarty/Data/mhc_ii/peptides/netMHCIIpan_input/HLADRB10101_positive.$length.fasta -length $length -a DRB1_0101 -xls -xlsfile /cellar/users/ramarty/Data/mhc_ii/binding_predictions/HLADRB10101_positive.$length.csv > /cellar/users/ramarty/Data/mhc_ii/binding_predictions/HLADRB10101_positive.length.txt
date
