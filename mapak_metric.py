import pandas as pd
from siamese_operations import format_siamese_output
from oracle_operations import filter_oracle
from files_operations import get_files_in_folder
import json
import os
import re

def formart_clone_to_dict(so_clone):
    so_clone = so_clone.split('|')
    return {'file1': so_clone[0], 'start1': int(so_clone[1]), 'end1': int(so_clone[2])}

def get_qualitas_clones_in_dataframe_by_so_clone(so_clone, dataframe):
    df_matched_rows = dataframe[
        (dataframe['file1'] == so_clone['file1']) &
        (dataframe['start1'] == so_clone['start1']) &
        (dataframe['end1'] == so_clone['end1'])]
    df_matched_rows = df_matched_rows[['file2', 'start2', 'end2']]
    df_matched_rows.reset_index(drop=True, inplace=True)
    return df_matched_rows.values.tolist()

def precision_at_k(df: pd.DataFrame, k: int=3, y_test: str='y_actual', y_pred: str='y_recommended') -> float:
    """
    Function to compute precision@k for an input boolean dataframe
    
    Inputs:
        df     -> pandas dataframe containing boolean columns y_test & y_pred
        k      -> integer number of items to consider
        y_test -> string name of column containing actual user input
        y-pred -> string name of column containing recommendation output
        
    Output:
        Floating-point number of precision value for k items
    """
    # check we have a valid entry for k
    if k <= 0:
        raise ValueError('Value of k should be greater than 1, read in as: {}'.format(k))
    # check y_test & y_pred columns are in df
    if y_test not in df.columns:
        raise ValueError('Input dataframe does not have a column named: {}'.format(y_test))
    if y_pred not in df.columns:
        raise ValueError('Input dataframe does not have a column named: {}'.format(y_pred))
        
    # extract the k rows
    dfK = df.head(k)
    # compute number of recommended items @k
    denominator = dfK[y_pred].sum()
    # compute number of recommended items that are relevant @k
    numerator = dfK[dfK[y_pred] & dfK[y_test]].shape[0]
    # return result
    if denominator > 0:
        return numerator/denominator
    else:
        return None

def recall_at_k(df: pd.DataFrame, k: int=3, y_test: str='y_actual', y_pred: str='y_recommended') -> float:
    """
    Function to compute recall@k for an input boolean dataframe
    
    Inputs:
        df     -> pandas dataframe containing boolean columns y_test & y_pred
        k      -> integer number of items to consider
        y_test -> string name of column containing actual user input
        y-pred -> string name of column containing recommendation output
        
    Output:
        Floating-point number of recall value for k items
    """
    # check we have a valid entry for k
    if k <= 0:
        raise ValueError('Value of k should be greater than 1, read in as: {}'.format(k))
    # check y_test & y_pred columns are in df
    if y_test not in df.columns:
        raise ValueError('Input dataframe does not have a column named: {}'.format(y_test))
    if y_pred not in df.columns:
        raise ValueError('Input dataframe does not have a column named: {}'.format(y_pred))
        
    # extract the k rows
    dfK = df.head(k)
    # compute number of all relevant items
    denominator = df[y_test].sum()
    # compute number of recommended items that are relevant @k
    numerator = dfK[dfK[y_pred] & dfK[y_test]].shape[0]
    # return result
    if denominator > 0:
        return numerator/denominator
    else:
        return None

open('error_siamese_execution.txt', 'w').write('')

writer = pd.ExcelWriter('mapak_results.xlsx', engine='xlsxwriter')
# optimization_algorithms = ['grid_search', 'random_search', 'bayesian_search']
optimization_algorithms = ['grid_search']
df_clones = pd.read_csv('clones.csv')
df_clones = filter_oracle(df_clones)

for algorithm in optimization_algorithms:
    print(algorithm)
    directory = f'output_{algorithm}'
    all_results_siamese_csv = get_files_in_folder(directory)
    
    for index, result_siamese_csv in enumerate(all_results_siamese_csv):
        if result_siamese_csv == 'README.md':
            continue
        
        try:
            df_siamese = format_siamese_output(directory, result_siamese_csv)
            # so_clones_from_siamese = 
            df_siamese['clone'] = df_siamese['file1'] + '|' + df_siamese['start1'].astype(str) + '|' + df_siamese['end1'].astype(str)
            so_clones_from_siamese = df_siamese['clone'].drop_duplicates().tolist()
            for so_clone in so_clones_from_siamese:
                so_clone = formart_clone_to_dict(so_clone)
                qa_clones_from_siamese = get_qualitas_clones_in_dataframe_by_so_clone(so_clone, df_siamese)
                qa_clones_from_oracle = get_qualitas_clones_in_dataframe_by_so_clone(so_clone, df_clones)
                print('')
                
            # mrr_result = calculate_mrr(result_siamese_csv, df_siamese, df_clones)
        except:
            open('error_siamese_execution.txt', 'a').write(f'{result_siamese_csv}\n')
            print(f'error in {result_siamese_csv}')
            continue



 