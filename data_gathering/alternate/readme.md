1. shell script `alt_to_fastq.sh` and `alt_data_pull.sh` are generated from .ipynb
2. `alt_to_fastq.sh` is to convert each patient's .sra (patients are from dbgap) to a single fastq file by a program called fastq-dump
3. `alt_data_pull.sh` calls several .py
    - mapping to KIR --> dones by `/data_gathering/bin/`: `mapped to reference.py`, `convert_to_fastq.py`, `component collection.py`(for KIR and whole exome?)
    - do something like PING?
    - HLA-HD
4. `merge_results.py` seems to save k-mer features (four components????) to a dataframe and save to `.csv`
5. what is `to_fastq.sh` doing??