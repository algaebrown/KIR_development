import pandas as pd
import numpy as np

'''
To go through all of the alternate samples on the secure nodes and get their features for the KIR region.
'''

# Get sample names
def valid_barcode(x):
    try:
        x.index('TCGA')
        return True
    except:
        return False
def get_barcode(x):
    i = x.index('TCGA')
    return x[i:i+12]
def get_origin(x):
    try:
        if int(x.split('-')[3][:2]) > 9:
            return 'normal'
        else:
            return 'tumor'
    except:
        try:
            if x.split('-')[3] == 'NT' or x.split('-')[3] == 'NB':
                return 'normal'
            else:
                return 'tumor'
        except:
            return 'tumor'

manifest = pd.read_csv('/cellar/users/ramarty/Data/kir/TCGA/manifests/whole_exome.all_samples.tsv', sep='\t')
manifest['valid'] = manifest.filename.apply(valid_barcode)
manifest = manifest[manifest.valid]
manifest['barcode'] = manifest.filename.apply(get_barcode)
manifest['origin'] = manifest.filename.apply(get_origin)
normal = manifest[manifest.origin == 'normal']
normal = normal.drop_duplicates('id')
normal_samples = list(normal.id)
normal_barcodes = list(normal.barcode)

samples = normal_barcodes

components = [x.strip() for x in open('/cellar/users/ramarty/Data/kir/kmers/kmer_groups/component_and_four_mers.txt')]

categories = ['components_four_counts', 'components_four_kir_counts', 'components_four_kir_read_counts',
              'components_four_read_counts']

# for each category of components
for cat in categories:

    features, used_samples = [], []
    # for each sample
    for i, sample in enumerate(samples[:500]):

        try:
            values = [float(x.strip()) for x in open('/nrnb/users/ramarty/TCGA/exomes/{0}/features/{1}.txt'.format(sample, cat)).readlines()]
            values = np.array(values).astype(float)
            normalized_values = values / sum(values)
            features.append(normalized_values)

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

