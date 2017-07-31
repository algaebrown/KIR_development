#! /bin/csh
#$ -V
#$ -S /bin/csh
#$ -o /cellar/users/ramarty/Data/kir/sge-system_files
#$ -e /cellar/users/ramarty/Data/kir/sge-system_files
#$ -cwd
#$ -t 1-19
#$ -l h_vmem=1G
#$ -tc 100
#$ -l long
set samples=(164511a9-2f56-49e0-b5cf-9c4be32f8fc7 168dbd66-6537-48e5-9181-048c81ab9d28 9edb7315-7f83-4604-8651-a3d31e96c5c4 300008de-27f1-4b4b-9675-ac1f56495563 07659099-452a-4a1e-a2fe-6b06028d7d31 a3bc0472-b2a4-4dbe-a125-185221c33510 b451ccf6-06dc-4d9a-8d92-68a01ef3ee07 fb3343c0-1298-4979-a4da-e1f087a85948 74ac1dad-7f3b-4a82-a787-e2e9f4083976 63e9eafb-d881-4613-9bfd-468daecb5170 5a5992b0-49ac-432d-8cd7-352dc71cf5da b003eef0-0050-4ac5-9851-9ffa89b0339c 658744b4-107f-4714-8a3a-e74d0350f29c 1e1bfb08-2cba-4b02-8777-fdec6575f92a 2d0fadf7-24cb-41d5-b554-01a77d006471 f3178ec2-9d0d-498d-aeca-94a0b5f202e4 09377f19-f96b-4593-ac64-6d567ffed251 86919607-d612-426e-ace0-ffa631d4b2a0 211c2a52-3213-4fe1-a45c-f51eb0b23e81)
set barcodes=(TCGA-HC-7737 TCGA-C4-A0F0 TCGA-21-1083 TCGA-KO-8416 TCGA-D3-A8GK TCGA-S7-A7WO TCGA-HI-7171 TCGA-FG-8185 TCGA-AX-A05W TCGA-BJ-A28R TCGA-FE-A235 TCGA-AL-3468 TCGA-AO-A03T TCGA-CF-A1HR TCGA-XF-A8HF TCGA-AB-2893 TCGA-VQ-A8E2 TCGA-25-2397 TCGA-55-6982)
set outs=(/nrnb/users/ramarty/TCGA/exomes/TCGA-HC-7737 /nrnb/users/ramarty/TCGA/exomes/TCGA-C4-A0F0 /nrnb/users/ramarty/TCGA/exomes/TCGA-21-1083 /nrnb/users/ramarty/TCGA/exomes/TCGA-KO-8416 /nrnb/users/ramarty/TCGA/exomes/TCGA-D3-A8GK /nrnb/users/ramarty/TCGA/exomes/TCGA-S7-A7WO /nrnb/users/ramarty/TCGA/exomes/TCGA-HI-7171 /nrnb/users/ramarty/TCGA/exomes/TCGA-FG-8185 /nrnb/users/ramarty/TCGA/exomes/TCGA-AX-A05W /nrnb/users/ramarty/TCGA/exomes/TCGA-BJ-A28R /nrnb/users/ramarty/TCGA/exomes/TCGA-FE-A235 /nrnb/users/ramarty/TCGA/exomes/TCGA-AL-3468 /nrnb/users/ramarty/TCGA/exomes/TCGA-AO-A03T /nrnb/users/ramarty/TCGA/exomes/TCGA-CF-A1HR /nrnb/users/ramarty/TCGA/exomes/TCGA-XF-A8HF /nrnb/users/ramarty/TCGA/exomes/TCGA-AB-2893 /nrnb/users/ramarty/TCGA/exomes/TCGA-VQ-A8E2 /nrnb/users/ramarty/TCGA/exomes/TCGA-25-2397 /nrnb/users/ramarty/TCGA/exomes/TCGA-55-6982)

set sample=$samples[$SGE_TASK_ID]
set barcode=$barcodes[$SGE_TASK_ID]
set out=$outs[$SGE_TASK_ID]

date
hostname
mkdir $out
bash /cellar/users/ramarty/Projects/kir/KIR_development/data_gathering/bin/GDC.exome.sh $sample $out/full_exome.bam
python /cellar/users/ramarty/Projects/kir/KIR_development/data_gathering/bin/convert_to_fastq.py $out/full_exome.bam $out/full_exome.fastq cellar
python /cellar/users/ramarty/Projects/kir/KIR_development/data_gathering/bin/convert_to_fastq2.py $out/full_exome.bam $out/full_exome_1.fastq $out/full_exome_1.fastq cellar
date
