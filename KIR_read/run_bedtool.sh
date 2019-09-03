short_id=$1
input_bam=/nrnb/users/ramarty/TCGA/exomes/$short_id/KIR_and_unmapped.aligned.bam

ref_bed=/cellar/users/hsher/Data/KIR_reference/all_alleles_and_random.bed
ref_genome=/cellar/users/hsher/Data/KIR_reference/all_alleles_and_random.tsv


# convert bam to bed
bedtools bamtobed -i $input_bam > /cellar/users/hsher/Data/tcga_bed/$short_id.bed

# run bedtool coverage: depth and breath of each KIR gene
bedtools coverage -b /cellar/users/hsher/Data/tcga_bed/$short_id.bed -a $ref_bed > /cellar/users/hsher/Data/KIR_coverage/$short_id
