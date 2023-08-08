import pandas as pd
from siamese_operations import format_siamese_output
from oracle_operations import filter_oracle
import json
import os
import re


def find_float_numbers(input_string):
    float_numbers = re.findall(r'\b\d+\.\d+\b', input_string)
    return [float(num) for num in float_numbers]


def extract_text_between_hyphens_and_underscores(input_string):
    pattern = r'-(.*?)\_'
    matches = re.findall(pattern, input_string)
    return matches

def get_files_in_folder(folder_path):
    files = os.listdir(folder_path)
    file_times = [(os.path.join(folder_path, file), os.path.getctime(os.path.join(folder_path, file))) for file in files]
    sorted_files = sorted(file_times, key=lambda x: x[1])
    return [file_path.split('/')[-1] for file_path, _ in sorted_files]


def check_clone_is_correct(oracle_clones_list, siamese_clone):
    siamese_clone = {'start2': siamese_clone[1], 'end2': siamese_clone[2]}
    
    for oracle_clone in oracle_clones_list:
        oracle_clone = {'start2': oracle_clone[1], 'end2': oracle_clone[2]}

        # Oracle inside Siamese
        start2_condition = oracle_clone['start2'] >= siamese_clone['start2']
        end2_condition = oracle_clone['end2'] <= siamese_clone['end2']

        if start2_condition and end2_condition:
            return True
            
        # Siamese inside Oracle
        start2_condition = oracle_clone['start2'] <= siamese_clone['start2']
        end2_condition = oracle_clone['end2'] >= siamese_clone['end2']

        if start2_condition and end2_condition:
            return True

    return False


def get_qualitas_clones_in_dataframe_by_so_clone(so_clone, dataframe):
    file1_cond = (dataframe['file1'] == so_clone['file1'])
    start1_cond = (dataframe['start1'] == so_clone['start1'])
    end1_cond = (dataframe['end1'] == so_clone['end1'])
    df_matched_rows = dataframe[file1_cond & start1_cond & end1_cond]
    df_matched_rows = df_matched_rows[['file2', 'start2', 'end2']]
    df_matched_rows.reset_index(drop=True, inplace=True)
    return df_matched_rows.values.tolist()


def merge_stackoverflow_clones(df_clones, df_siamese):
    df_siamese_filtered = df_siamese[['file1', 'start1', 'end1']]
    df_siamese_queries = df_siamese_filtered.drop_duplicates(subset=['file1', 'start1', 'end1'])

    df_clones_filtered = df_clones[['file1', 'start1', 'end1']]
    df_clones_queries = df_clones_filtered.drop_duplicates(subset=['file1', 'start1', 'end1'])
    
    
    return pd.merge(df_siamese_queries, df_clones_queries, on=['file1', 'start1', 'end1'])


def calculate_mrr(df_siamese, df_clones):
    # File1 -> Stackoverflow 
    # File2 -> Qualitas Corpus

    total_reciprocal_rank = 0.0
    merged_so_df = merge_stackoverflow_clones(df_clones, df_siamese)
    num_queries = df_clones.shape[0]

    for total_index, row in merged_so_df.iterrows():
        oracle_clones = get_qualitas_clones_in_dataframe_by_so_clone(row, df_clones)
        siamese_hit_attempts = get_qualitas_clones_in_dataframe_by_so_clone(row, df_siamese)
        for index, siamese_hit in enumerate(siamese_hit_attempts):
            clone_is_correct = check_clone_is_correct(oracle_clones, siamese_hit)

            if clone_is_correct:
                total_reciprocal_rank += 1/(index+1)
                break
            
            # This code is not necessary
            if (index + 1) == len(siamese_hit_attempts):
                total_reciprocal_rank += 0
                break

    mrr = total_reciprocal_rank/num_queries
    # print(f'Number of Queries (Num. SO Snippets): {num_queries}', f'MRR: {mrr}')
    return mrr


def calculate_one_mrr(directory, result_siamese_csv):
    df_siamese = format_siamese_output(directory, result_siamese_csv)
    df_clones = pd.read_csv('clones.csv')
    df_clones = filter_oracle(df_clones)
    return calculate_mrr(df_siamese, df_clones)


def calculate_complete_mrr():
    df_clones = pd.read_csv('clones.csv')
    df_clones = filter_oracle(df_clones)
    optimization_algorithms = ['grid_search', 'random_search', 'bayesian_search']
    columns = ['index', 'cloneSize', 'ngramSize', 'qrNorm', 'boost', 'time', 'mrr']
    writer = pd.ExcelWriter('mrr_results.xlsx', engine='xlsxwriter')

    for algorithm in optimization_algorithms:
        print(algorithm)
        directory = f'output_{algorithm}'
        results_siamese_csv = get_files_in_folder(directory)

        mrr_by_siamese_result = {}
        mrr_results_by_algorithm = []
        all_result_time = open(f'./{algorithm}_result_time.txt', 'r').read()
        result_time = list(map(float, find_float_numbers(all_result_time)))

        for index, result_siamese_csv in enumerate(results_siamese_csv):
            if result_siamese_csv == 'README.md':
                continue

            try:
                df_siamese = format_siamese_output(directory, result_siamese_csv)
                mrr_result = calculate_mrr(df_siamese, df_clones)
                mrr_by_siamese_result[result_siamese_csv] = mrr_result
            except:
                print(f'error in {result_siamese_csv}')


            params = extract_text_between_hyphens_and_underscores(result_siamese_csv)
            params = [int(num) for num in params]
            
            mrr_result_row = [index+1]
            for param in params:
                mrr_result_row.append(param)
            mrr_result_row.append(result_time[index])
            mrr_result_row.append(mrr_result)

            mrr_results_by_algorithm.append(mrr_result_row)

        with open(f'mrr_{algorithm}.json', "w") as json_file:
            json.dump(mrr_by_siamese_result, json_file, indent=4)
        
        df_metric = pd.DataFrame(mrr_results_by_algorithm, columns=columns)
        df_metric.to_excel(f'mrr_{algorithm}.xlsx', index=False)
        df_metric.to_excel(writer, sheet_name=algorithm, index=False)

    writer.close()
