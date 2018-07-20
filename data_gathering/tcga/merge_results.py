import pandas as pd
import numpy as np

'''
To go through all of the alternate samples on the secure nodes and get their features for the KIR region.
'''

def get_TARGET(x):
    if 'TARGET' in x:
        return True
    else:
        return False
def get_origin(x):
    return int(x.split('-')[3][:2])

uuid_barcode_map = pd.read_csv('/cellar/users/andreabc/GDC_barcodes/uuid_barcode_map.txt', sep='\t')

# only exome
uuid_barcode_map = uuid_barcode_map[uuid_barcode_map.type == 'aligned_reads']
# remove target
uuid_barcode_map['TARGET'] = uuid_barcode_map.sample_barcode.apply(get_TARGET)
uuid_barcode_map = uuid_barcode_map[~uuid_barcode_map['TARGET']]

uuid_barcode_map['origin'] = uuid_barcode_map.sample_barcode.apply(get_origin)
uuid_barcode_map = uuid_barcode_map[uuid_barcode_map.origin.isin([10, 11])]

uuid_barcode_map = uuid_barcode_map.drop_duplicates('barcode')

samples = list(uuid_barcode_map.barcode)


components = [x.strip() for x in open('/cellar/users/ramarty/Data/kir/kmers/kmer_groups/kir_four_random.txt')]

categories = ['kir_four_random_counts', 'kir_four_random_read_counts']

# for each category of components
for cat in categories:

    features, used_samples = [], []
    # for each sample
    for i, sample in enumerate(samples):

        try:
            values = [float(x.strip()) for x in open('/nrnb/users/ramarty/TCGA/exomes/{0}/features/{1}.txt'.format(sample, cat)).readlines()]
            values = np.array(values).astype(float)
            features.append(values)
            #normalized_values = values / sum(values)
            #features.append(normalized_values)

            used_samples.append(sample)
            print i, sample

        except:
            None

    # merge all of them
    df = pd.DataFrame(features)
    print len(df.columns), len(df.index)

    df.columns = components
    df.index = used_samples

    df.to_csv('/cellar/users/ramarty/Data/kir/components/tcga/{0}.csv'.format(cat))

