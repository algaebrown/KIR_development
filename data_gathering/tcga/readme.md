1. `exon_data_pull.ipynb` generates scripts to download TCGA .bam, stripped the wanted region, remap to KIR, and generate k-mer per patient
2. `components_construction.ipynb` makes the k-mer file for KIR genes, random genes so that the we can count their occurence in the selected reads.
3. `normalization_genes.ipynb` picks the 100 random gene, extract their chromosomal location for `exon_data_pull` to work.
4. `creating_all_the_good_stuff.ipynb` makes neoantigen, immune type, CIBERSORT and KIR types altogether.
5. `gathering_clinical_data.ipynb` extracts clinical information (tumor type from patient)


Nearly all the .sh file are generated from `exon_data_pull.ipynb` to submit jobs to the cluster.

Questions:
1. where do the single file, 1 row per sample, 1 coloum per k-mer file come from?