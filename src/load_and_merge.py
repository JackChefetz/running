import os
import pandas as pd

def load_and_merge():
    """Loads and merges all csv files in specified directory"""
    data_path = '../data/all/'
    dfs = []
    for filename in os.listdir(data_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(data_path, filename)
            df = pd.read_csv(file_path)
            dfs.append(df)    
    all = pd.concat(dfs, ignore_index=True)
    
    # Remove duplicate rows
    all = all.drop_duplicates()

    # filter to only running
    all = all[all['Activity Type'] == 'Running']

    # format location text
    all['Location'] = all['Title'].str.replace('Running', '').str.strip()

    # date/time conversions
    all['Date'] = pd.to_datetime(all['Date'])
    
    return all
