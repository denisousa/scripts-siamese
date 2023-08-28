import pandas as pd
from siamese_operations import format_siamese_output
from oracle_operations import filter_oracle
from files_operations import get_files_in_folder
from test_mapak_metric import calculate_map_at_k
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

    df_matched_rows['clone'] = df_matched_rows['file2'] + '|' + df_matched_rows['start2'].astype(str) + '|' + df_matched_rows['end2'].astype(str)

    df_matched_rows.reset_index(drop=True, inplace=True)
    return df_matched_rows['clone'].values.tolist()

open('error_siamese_execution.txt', 'w').write('')

writer = pd.ExcelWriter('mapak_results.xlsx', engine='xlsxwriter')
# optimization_algorithms = ['grid_search', 'random_search', 'bayesian_search']
optimization_algorithms = ['grid_search']
df_clones = pd.read_csv('clones.csv')
df_clones = filter_oracle(df_clones)

mapak = {'erro': 0}

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
                
                if len(qa_clones_from_oracle) == 0:
                    mapak['erro'] += 1
                
                k = len(qa_clones_from_oracle)
                try:
                    mapak[k].append([qa_clones_from_oracle, qa_clones_from_siamese])
                except:
                    mapak[k] = [qa_clones_from_oracle, qa_clones_from_siamese]

            #k = 2
            #map_at_k = calculate_map_at_k(actual_list, predicted_list, k)
            #print(f"MAP@{k} = {map_at_k:.4f}")

                
            # mrr_result = calculate_mrr(result_siamese_csv, df_siamese, df_clones)
        except:
            open('error_siamese_execution.txt', 'a').write(f'{result_siamese_csv}\n')
            print(f'error in {result_siamese_csv}')
            continue


print('')