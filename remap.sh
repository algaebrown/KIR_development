re
# input .sra
# convert to fastq
# map to GR 35
# samtool extract three and then merge
# map to KIR reference
# collect k-mer

sra_file=$1 # SRA102983
sra_path=$2 # /nrnb folder to contain fastq
output_path=$3

echo "convert to fastq"


faster=/cellar/users/andreabc/software/sratoolkit.2.9.2-ubuntu64/bin/fasterq-dump

$faster --concatenate-reads $sra_path$sra_file.sra -e 8 -o $sra_path$sra_file.fastq

# map to GRCh38

GRCh38=/cellar/users/hsher/Data/reference/GRCh38.d1.vd1.fa.tar.gz

bowtie2=/cellar/users/ramarty/programs/bowtie2-2.2.9/bowtie2

$bowtie2 -k 1 -x $GRCh38 -U $sra_path$sra_file.fastq -b $output_path$sra_file.bam

# select the KIR region, random genes and unmapped reads

samtools=/cellar/users/hcarter/programs/samtools-1.2/samtools

$samtools view -b $output_path$sra_file.bam chr19:54025634-55084318 > $output_path$sra_file.kir.bam

# select the unmapped
$samtools view -b -f 4 $output_path$sra_file.bam > $output_path$sra_file.unmapped.bam

# merge the two .bam file
$samtools merge $output_path$sra_file.merged.bam $output_path$sra_file.kir.bam $output_path$sra_file.unmapped.bam

# delete the seperate files
rm $output_path$sra_file.kir.bam
rm $output_path$sra_file.unmapped.bam

# sort bam, remove deduplicates, and make to fastq
$samtools sort -n $output_path$sra_file.merged.bam > $output_path$sra_file.sorted.bam

rm $output_path$sra_file.merged.bam

$samtools rmdup $output_path$sra_file.sorted.bam $output_path$sra_file.dedup.bam

rm $output_path$sra_file.sorted.bam

bedtools=/cellar/users/hcarter/programs/bedtools-2.17.0/bin/bamToFastq

$bedtools -i $output_path$sra_file.dedup.bam -fq $output_path$sra_file.selected.fastq

# realign to KIR alleles and 
kir_ref=/cellar/users/ramarty/Data/kir/ref/all_alleles_and_random

$bowtie2 -k 1 -x $kir_ref -U $output_path$sra_file.selected.fastq | $samtools view -bS -h -F 4 - > $output_path$sra_file.aligned.bam

# sort and convert to fastq
$samtools sort -n $output_path$sra_file.aligned.bam > $output_path$sra_file.aligned.sorted.bam 

$bedtools -i $output_path$sra_file.aligned.sorted.bam -fq $output_path$sra_file.aligned.fastq


# collect k-mer
get_kmer=/cellar/users/ramarty/Projects/kir/KIR_development/data_gathering/bin/component_collection.py

kmer=/cellar/users/ramarty/Data/kir/kmers/kmer_groups/kir_four_random.txt

python $get_kmer $output_path$sra_file.aligned.fastq $output_path $kmer $sra_file
