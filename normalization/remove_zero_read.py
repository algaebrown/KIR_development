# remove zero reads
import pandas as pd
def remove_zero_read(read_file = '~/Data/reads_summary.csv'):
    """
    remove sample with zero reads mapped to KIR
    input: file containing read information
    return(short_id_list)
    """
    df = pd.read_csv(read_file, index_col = 0, header = 0)
    selected_id = df.loc[df['KIR_total_read'] > 0].index

    return(selected_id)
