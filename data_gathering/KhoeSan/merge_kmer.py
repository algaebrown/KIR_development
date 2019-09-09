import pandas as pd
import numpy as np

def merge_kmer(components, categories, sample_dir, samples, output_dir):
    '''
    to merge kmer from individual kmer files for each sample generated from `components_collection.py`
    :param components: kmers, serve as header; sample file at /cellar/users/ramarty/Data/kir/kmers/kmer_groups/component_and_four_mers.txt
    :param categories: based on how the numbers are calculated. sample are 'components_four_counts', 'components_four_kir_counts', 'components_four_kir_read_counts','components_four_read_counts'] make a list to specify what you want to calculate
    :param sample_feature_dir: specify the list of diretory of the 'components_four_counts.txt': /nrnb/users/ramarty/kir/PING/KhoeSan/sra/SRR1171017/features
    :param output_dir: where the merged file should go
    '''
    
    # for each category of components
    for cat in categories:

        features, used_samples = [], []
        # for each sample
        for s in samples:

            try:
                # read the kmers for each sample
                values = [float(x.strip()) for x in open(sample_dir + s + '/features/'  + cat + '.txt').readlines()]
                values = np.array(values).astype(float)
            
                # list in list of k=mers
                features.append(values)
            

                used_samples.append(s)
                print (s)

            except:
                None
        
        # merge all of them
        df = pd.DataFrame(features)
        print (len(df.columns), len(df.index))
    
        # set columns as kmers
        df.columns = components
        # set index as sample id
        df.index = used_samples

        df.to_csv(output_dir + cat + '.csv')

    