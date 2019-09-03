def four_mer(file = '/cellar/users/ramarty/Data/kir/kmers/kmer_groups/four_mers.txt'):
    return([x.strip() for x in open(file).readlines()])

def four_mer_coverage(df, four_mer):
    '''
    :param df: dataframe containing k-mer counts
    :param four_mer: all 4-mers
    return 4-mer counts (estimates coverage) series
    '''
    return(df[four_mer].sum(axis = 1))


    
    
