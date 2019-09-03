# to read KIR and random genes from bedtool outputs

import pandas as pd
def read_kir_allele(file = '/cellar/users/hsher/Data/KIR_reference/KIR_annotation.tsv'):
    """
    To read KIR allele information (which allele belong to which gene, IPD ID, including random genes)
    :params: file: default to the /hsher/Data/KIR_reference/KIR_annotation.tsv
    """
    kir_anno = pd.read_csv(file, header = 0, index_col = 0, sep = '\t')

    # additional column to pick out KIR genes
    kir_anno.loc[kir_anno['gene'].str.contains('KIR'), 'is_kir'] = True
    kir_anno.fillna(False, inplace = True)

    return(kir_anno)

kir_anno = read_kir_allele()
anchor_genes = ['KIR3DL3', 'KIR3DP1', 'KIR2DL4', 'KIR3DL2']

def read_bed_coverage(short_id):
    '''
    read `bedtool coverage -b SHORT_ID_.bam -a reference.bed` output file
    input SHORT ID name
    return data frame with rows = KIR allele, index = IPD_ID, columns = read(how many reads map to that region), breadth(% of region covered by at least 1 read)
    '''
    base = '/cellar/users/hsher/Data/KIR_coverage/'
    df = pd.read_csv(base + short_id, header = None, sep = '\t', index_col = 0, names = ['gene_id','kir_start', 'kir_end', 'reads', 'length', 'total_length', 'breadth'])

    return(df[['reads', 'breadth']])

def KIR_no_reads(df):
    '''
    return # of read mapped to KIR alleles
    '''
    return(df.loc[kir_anno['is_kir'], 'reads'].sum())

def random_no_reads(df):
    '''
    return # of read mapped to random genes
    '''
    return(df.loc[~kir_anno['is_kir'], 'reads'].sum())

def each_KIR_reads(df):
    '''
    return reads mapped to each anchoring gene
    '''
    anchor_count = []
    anchor_max_two_allele = []
    anchor_max_breadth_allele = []
    anchor_max_read = []
    anchor_max_breadth = []
    for a_gene in anchor_genes:
        IPD_index = kir_anno.loc[kir_anno['gene']== a_gene].index
        anchor_count.append(df.loc[IPD_index,'reads'].sum())
        anchor_max_read.append(df.loc[IPD_index,'reads'].max())
        anchor_max_breadth.append(df.loc[IPD_index,'breadth'].sum())
        anchor_max_two_allele += df.loc[IPD_index,'reads'].nlargest(n= 2).index.tolist()
        anchor_max_breadth_allele += df.loc[IPD_index,'breadth'].nlargest(n= 2).index.tolist()
    return(anchor_count,anchor_max_read,anchor_max_breadth, anchor_max_two_allele, anchor_max_breadth_allele)

def run_all_property(short_id):
    """
    get all property for SINGLE sample (short_id)
    """

    print(short_id)
    
    df = read_bed_coverage(short_id)
    random_reads = random_no_reads(df)
    kir_reads = KIR_no_reads(df)

    anchor_count, anchor_max_read, anchor_max_breadth, anchor_max_two_allele, anchor_max_breadth_allele = each_KIR_reads(df)
    
    
    return(random_reads, kir_reads, anchor_count, anchor_max_read, anchor_max_breadth, anchor_max_two_allele, anchor_max_breadth_allele, short_id)

from multiprocessing import Manager, Pool



def retrieve_all_property(short_id_list, thread = 8):



    # start threads
    with Pool(thread) as p:
        results = p.map(run_all_property, short_id_list)

    

    # initialize dataframe
    sum_stats = pd.DataFrame(index = short_id_list, columns = ['KIR_total_read', 'random_total_read']+
                [a_gene+'total_read' for a_gene in anchor_genes]+
                [a_gene+'max_read' for a_gene in anchor_genes]+
                [a_gene+'max_breadth' for a_gene in anchor_genes]+
                [a_gene+'max_read_allele_' + str(y) for a_gene in anchor_genes for y in range(1,3)]+
                [a_gene+'max_breadth_allele_'+ str(y) for a_gene in anchor_genes for y in range(1,3)])

    # save results
    for r in results:
        short_id = r[-1]
        sum_stats.loc[short_id, 'KIR_total_read'] = r[1]
        sum_stats.loc[short_id, 'random_total_read'] = r[0]
        sum_stats.loc[short_id, [a_gene+'total_read' for a_gene in anchor_genes]] = r[2]
        sum_stats.loc[short_id, [a_gene+'max_read' for a_gene in anchor_genes]] = r[3]
        sum_stats.loc[short_id, [a_gene+'max_breadth' for a_gene in anchor_genes]] = r[4]

        sum_stats.loc[short_id, [a_gene+'max_read_allele_' + str(y) for a_gene in anchor_genes for y in range(1,3)]] = r[5]
        sum_stats.loc[short_id, [a_gene+'max_breadth_allele_' + str(y) for a_gene in anchor_genes for y in range(1,3)]] = r[6]

    return(sum_stats)
