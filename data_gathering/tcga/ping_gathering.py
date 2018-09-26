import pandas as pd
import numpy as np

df = pd.read_csv('/cellar/users/ramarty/Data/kir/validation/PING/run_time.csv', index_col=0)
barcodes = list(df.Barcode)


all_dfs = []
for barcode in barcodes:

    data = pd.read_csv('/nrnb/users/ramarty/TCGA/exomes/{0}/PING/MIRA_results.csv'.format(barcode), index_col=0)

    data[barcode] = data.__KIR

    all_dfs.append(data.loc[:, ['barcode']].transpose())


merged = pd.concat(all_dfs)

merged.to_csv('/cellar/users/ramarty/Data/kir/validation/PING/results.csv')