#! /bin/csh
#$ -V
#$ -S /bin/csh
#$ -o /cellar/users/ramarty/Data/kir/sge-system_files
#$ -e /cellar/users/ramarty/Data/kir/sge-system_files
#$ -cwd
#$ -t 1-18
#$ -l h_vmem=30G
#$ -tc 30
#$ -l long
set samples=(SRR1171049 SRR1171058 SRR1175182 SRR1258307 SRR1171017 SRR1171051 SRR1175179 SRR1175183 SRR1265483 SRR1171020 SRR1171052 SRR1175180 SRR1175184 SRR1265484 SRR1171021 SRR1171056 SRR1175181 SRR1258307)
set outs=(/nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1171049 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1171058 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1175182 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1258307 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1171017 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1171051 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1175179 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1175183 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1265483 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1171020 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1171052 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1175180 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1175184 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1265484 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1171021 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1171056 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1175181 /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1258307)

set sample=$samples[$SGE_TASK_ID]
set out=$outs[$SGE_TASK_ID]

date
hostname
mkdir $out
mkdir $out/features
mv $out.fastq $out/full_exome.fastq
python /cellar/users/ramarty/Projects/kir/KIR_development/data_gathering/bin/map_to_reference.py $out/full_exome.fastq $out/full_exome_kir.bam /cellar/users/ramarty/Data/kir/ref/all_alleles cellar
echo Mapped to KIR.
python /cellar/users/ramarty/Projects/kir/KIR_development/data_gathering/bin/convert_to_fastq.py $out/full_exome_kir.bam $out/full_exome_kir.fastq
echo Stripped reads.
python /cellar/users/ramarty/Projects/kir/KIR_development/data_gathering/bin/component_collection.py $out/full_exome_kir.fastq $out/features /cellar/users/ramarty/Data/kir/kmers/kmer_groups/component_and_four_mers.txt components_four_kir
echo Components gathered - KIR.
python /cellar/users/ramarty/Projects/kir/KIR_development/data_gathering/bin/component_collection.py $out/full_exome.fastq $out/features /cellar/users/ramarty/Data/kir/kmers/kmer_groups/component_and_four_mers.txt components_four
echo Components gathered - whole exome.
rm $out/full_exome_kir.fastq
rm $out/full_exome_sorted*
rm $out/full_exome*bam
date
