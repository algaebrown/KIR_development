import pandas as pd
def kir_kmer():
    """
    read all KIR specific k-mer
    :param file containing k-mer
    return dictionary in dictionary, first layer keys are the length of k-mer; second layer of keys is the KIR gene name
    """
    import json
    kmers = {}
    ks = [10, 15, 20, 25, 30, 35, 40]
    for k in ks:
        with open('/cellar/users/ramarty/Data/kir/kmers/gene_grouped_kmers/{0}.txt'.format(str(k))) as infile:
            g = json.load(infile)
            kmers[k] = g
    return(kmers)

def kmer_df(kir_kmer):
    df = pd.DataFrame(columns = ['kmer', 'length', 'gene'])        
    all_kmer = []
    i=0
    for length in kir_kmer.keys():
        for gene in kir_kmer[length].keys():
            for kmer in kir_kmer[length][gene]:
                df.loc[i] = [kmer, length, gene]
                i += 1
    
    return(df)
def GC_content(kmer):
    """
    return GC content of kmer
    """
    return((kmer.count('C')+kmer.count('G'))/len(kmer))

def select_qualified_kmer(kmer_list, lower_bound = 0.4, upper_bound = 0.65):
    """
    return k-mer with qualified GC content
    :param kmer_list: list of k-mers
    :param lower_bound: defalut 0.4
    :param upper_bound: default 0.65
    return k-mers list
    """
    gc = pd.Series(kmer_list).apply(GC_content)
    gc.index = kmer_list

    return(gc.loc[gc >= lower_bound].loc[gc <= upper_bound].index)

