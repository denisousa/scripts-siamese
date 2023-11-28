import pandas as pd
from siamese_operations import format_siamese_output
from oracle_operations import filter_oracle
from parameters_operations import get_parameters_in_dict
import copy
import json
import os
import re
import numpy as np


def find_lines_with_specific_text(filename, text):
    result = []
    with open(filename, 'r') as file:
        for line in file:
            if text in line:
                result.append(line.strip().replace(text, '').strip())
    return result

def get_k_hits(recommended_items, relevant_items):
    recommended_and_relevant = []

    hit = []

    for index, item in enumerate(recommended_items):
        if len(recommended_and_relevant) == len(relevant_items):
            break

        check, relevant_hit = check_clone_is_correct(relevant_items, item)
        if check:
            recommended_and_relevant.append(item) 
            hit.append(index+1)
       
    return f'{hit}'

def precision_at_k(recommended_items, relevant_items, k):
    recommended_items = recommended_items[:k]
    recommended_and_relevant = []

    for index, item in enumerate(recommended_items):
        if len(recommended_and_relevant) == len(relevant_items):
            break

        check, relevant_hit = check_clone_is_correct(relevant_items, item)
        if check:
            recommended_and_relevant.append(item)
       
    return round(len(recommended_and_relevant) / k, 2)

def recall_at_k(recommended_items, relevant_items, k):
    recommended_items = recommended_items[:k]
    recommended_and_relevant = []

    hit = []

    for index, item in enumerate(recommended_items):
        if len(recommended_and_relevant) == len(relevant_items):
            break

        check, relevant_hit = check_clone_is_correct(relevant_items, item)
        if check:
            recommended_and_relevant.append(item)
            hit.append(index+1)
    
    return round(len(recommended_and_relevant) / len(relevant_items), 2)

def apk(recommended_items, relevant_items, k):
    precisions = [precision_at_k(recommended_items, relevant_items, i) for i in range(1, k+1)]
        
    return round(sum(precisions) / k, 2)

def mapk(recommended_items, relevant_items, k):
    return round(np.mean([apk(a,p,k) for a,p in zip(recommended_items, relevant_items)]),2)

def find_float_numbers(input_string):
    float_numbers = re.findall(r'\b\d+\.\d+\b', input_string)
    return [float(num) for num in float_numbers]

def find_lines_with_runtime(filename):
    result = []
    with open(filename, 'r') as file:
        for line in file:
            if 'Runtime:' in line:
                result.append(line.strip().replace('Runtime: ', ''))
    return result

def get_files_in_folder(folder_path):
    files = os.listdir(folder_path)
    file_times = [(os.path.join(folder_path, file), os.path.getctime(os.path.join(folder_path, file))) for file in files]
    sorted_files = sorted(file_times, key=lambda x: x[1])
    return [file_path.split('/')[-1] for file_path, _ in sorted_files]

def check_clone_is_correct(oracle_clones_list, siamese_clone):
    siamese_clone = {'file2': siamese_clone[0], 'start2': siamese_clone[1], 'end2': siamese_clone[2]}
    
    for oracle_clone in oracle_clones_list:
        oracle_clone = {'file2': oracle_clone[0], 'start2': oracle_clone[1], 'end2': oracle_clone[2]}

        file2_condition = oracle_clone['file2'] == siamese_clone['file2']

        # Oracle inside Siamese
        start2_condition = oracle_clone['start2'] >= siamese_clone['start2']
        end2_condition = oracle_clone['end2'] <= siamese_clone['end2']

        if file2_condition and start2_condition and end2_condition:
            return True, list(oracle_clone.values())
            
        # Siamese inside Oracle
        start2_condition = oracle_clone['start2'] <= siamese_clone['start2']
        end2_condition = oracle_clone['end2'] >= siamese_clone['end2']

        if file2_condition and start2_condition and end2_condition:
            return True, list(oracle_clone.values())

    return False, list(oracle_clone.values())

def get_qualitas_clones_in_dataframe_by_so_clone(so_clone, dataframe):
    df_matched_rows = dataframe[
        (dataframe['file1'] == so_clone['file1']) &
        (dataframe['start1'] == so_clone['start1']) &
        (dataframe['end1'] == so_clone['end1'])]
    df_matched_rows = df_matched_rows[['file2', 'start2', 'end2']]
    df_matched_rows.reset_index(drop=True, inplace=True)
    return df_matched_rows.values.tolist()

def get_problemns_in_oracle(df_clones):
    problems_in_oracle = {}

    file1_oracles = df_clones['file1'].tolist()

    unique_files = [i for i in file1_oracles if file1_oracles.count(i)==1]
    len_unique = len([i for i in file1_oracles if file1_oracles.count(i)==1])
    problems_in_oracle['unique_files'] = unique_files

    duplicate_files_list_by_one = [x for i, x in enumerate(file1_oracles) if i != file1_oracles.index(x)]
    duplicate_files_list = list(set(duplicate_files_list_by_one))

    so_clones = df_clones[['file1','start1','end1']]
    duplicate_clones_oracle = so_clones[so_clones.duplicated()]
    exact_clones_oracle = duplicate_clones_oracle.drop_duplicates()
    problems_in_oracle['exact_clones'] = exact_clones_oracle.values.tolist()

    count_duplicastes_clones = 0
    problems_in_oracle['duplicate_files'] = {}
    for row, duplicate_files in enumerate(duplicate_files_list):
        df = df_clones[df_clones['file1'] == duplicate_files]
        df = df.reset_index(drop=True)
        count_duplicastes_clones += df.shape[0]
        try:
            problems_in_oracle['duplicate_files'][df.shape[0]]['amount'] += 1
            problems_in_oracle['duplicate_files'][df.shape[0]]['example'].append(df[['file1', 'start1', 'end1']].values.tolist())
        except:
            problems_in_oracle['duplicate_files'][df.shape[0]] = {}
            problems_in_oracle['duplicate_files'][df.shape[0]]['amount'] = 1
            problems_in_oracle['duplicate_files'][df.shape[0]]['example'] = []
            problems_in_oracle['duplicate_files'][df.shape[0]]['example'].append(df[['file1', 'start1', 'end1']].values.tolist())


    problems_in_oracle['total'] = len_unique + count_duplicastes_clones 
    problems_in_oracle['unique'] = len_unique
    problems_in_oracle['repeat'] = count_duplicastes_clones
    # problems_in_oracle['total'] = len(duplicate_files_list_by_one)

    with open('problems_in_oracle.json', "w") as json_file:
        json.dump(problems_in_oracle, json_file, indent=2)
    return problems_in_oracle

def calculate_hit_number(all_reciprocal_rank, k):
    all_reciprocal_rank[f'status@{k}'] = {}

    if f'results_k@{k}' in all_reciprocal_rank:
        for rr in all_reciprocal_rank[f'results_k@{k}']:
            if f"hit_{rr['hit_number']}" in all_reciprocal_rank[f'status@{k}']:
                all_reciprocal_rank[f'status@{k}'][f"hit_{rr['hit_number']}"] += 1

            else:
                all_reciprocal_rank[f'status@{k}'][f"hit_{rr['hit_number']}"] = 1

    return all_reciprocal_rank

def get_so_clones_from_oracle(df_clones, df_siamese):
    exact_predict_data = []
    inside_predict_data = []
    not_predict_data = []

    df_siamese = df_siamese.drop_duplicates(subset=['file1', 'start1', 'end1'])

    for _, oracle_row in df_clones.iterrows():
        df_filtered = df_siamese[df_siamese['file1'] == oracle_row['file1']]

        if df_filtered.shape[0] == 0:
            not_predict_data.append({'file1': oracle_row['file1'],
                                     'start1': oracle_row['start1'],
                                     'end1': oracle_row['end1'],})
            
        for _, siamese_row in df_filtered.iterrows():
            if oracle_row['start1'] == siamese_row['start1'] and oracle_row['end1'] == siamese_row['end1']: 
                exact_predict_data.append(siamese_row)
                break

            elif oracle_row['start1'] >= siamese_row['start1'] and oracle_row['end1'] <= siamese_row['end1']: 
                inside_predict_data.append(siamese_row)
                break

            elif oracle_row['start1'] <= siamese_row['start1'] and oracle_row['end1'] >= siamese_row['end1']: 
                inside_predict_data.append(siamese_row)
                break

            else:
                print('problem')
            
    df_exact_predict = pd.DataFrame(exact_predict_data).sort_values(by='file1')
    df_exact_predict = df_exact_predict.drop_duplicates(subset=['file1', 'start1', 'end1'])

    try:
        df_inside_predict = pd.DataFrame(inside_predict_data).sort_values(by='file1')
        df_inside_predict = df_inside_predict.drop_duplicates(subset=['file1', 'start1', 'end1'])
    except:
        df_inside_predict = pd.DataFrame()

    try:
        df_not_predict = pd.DataFrame(not_predict_data).sort_values(by='file1')
        df_not_predict = df_not_predict.drop_duplicates(subset=['file1'])
    except:
        df_inside_predict = pd.DataFrame()

    df_concat_predict = pd.concat([df_exact_predict, df_inside_predict], ignore_index=True)
    
    df_exact_and_inside_predict = df_concat_predict[df_concat_predict.duplicated()]
    
    df_concat_predict = df_concat_predict.drop_duplicates(subset=['file1', 'start1', 'end1'])
    return {
        'correct_predictions': df_concat_predict,
        'exact_predictions': df_exact_predict,
        'inside_predictions': df_inside_predict,
        'exact_inside_predictions': df_exact_and_inside_predict,
        'not_predictions':df_not_predict
        }

def get_list_items_relevants(df_clones, clones_in_oracle, not_predicted_clones):
    relevants_clones = set()

    for _, row in clones_in_oracle.iterrows():
       oracle_clones = get_qualitas_clones_in_dataframe_by_so_clone(row, df_clones)
       relevants_clones.add(len(oracle_clones))
    
    for _, row in not_predicted_clones.iterrows():
        oracle_clones = get_qualitas_clones_in_dataframe_by_so_clone(row, df_clones)
        relevants_clones.add(len(oracle_clones))
    
    return list(relevants_clones)

def add_precision_recall_apk(rr, siamese_hit_attempts, oracle_clones, i):
    rr[f'Precision@{i}'] = precision_at_k(siamese_hit_attempts, oracle_clones, i)
    rr[f'Recall@{i}'] = recall_at_k(siamese_hit_attempts, oracle_clones, i)
    rr[f'APK@{i}'] = apk(siamese_hit_attempts, oracle_clones, i)
    return rr

def remove_precision_recall_apk(rr, i):
    del rr[f'Precision@{i}']
    del rr[f'Recall@{i}']
    del rr[f'APK@{i}']
    return rr

def calculate_metrics(result_siamese_csv, df_siamese, df_clones):
    # File1 -> Stackoverflow 
    # File2 -> Qualitas Corpus

    total_reciprocal_rank = 0.0
    # print(result_siamese_csv)
    
    so_clones = get_so_clones_from_oracle(df_clones, df_siamese)
    clones_in_oracle = so_clones['correct_predictions']
    not_predicted_clones = so_clones['not_predictions']
    
    df_queries = df_clones.drop_duplicates(subset=['file1', 'start1', 'end1'])
    num_queries = df_queries.shape[0]

    all_reciprocal_rank = {
        'siamese_status': { 
            'num_queries': num_queries,
            'predictions': clones_in_oracle.shape[0],
            'not_predict': not_predicted_clones.shape[0],
        },
        'parameters': get_parameters_in_dict(result_siamese_csv),
    }

    number_relevants_clones = get_list_items_relevants(df_clones, clones_in_oracle, not_predicted_clones)

    for _, row in clones_in_oracle.iterrows():
        reciprocal_rank = 0
        
        unique_so_clone = f"{row['file1']}_{row['start1']}_{row['end1']}"
        oracle_clones = get_qualitas_clones_in_dataframe_by_so_clone(row, df_clones)
        siamese_hit_attempts = get_qualitas_clones_in_dataframe_by_so_clone(row, df_siamese)

        for index, siamese_hit in enumerate(siamese_hit_attempts):

            clone_is_correct, _ = check_clone_is_correct(oracle_clones, siamese_hit)
            if clone_is_correct:
                reciprocal_rank += 1/(index+1)
                total_reciprocal_rank += 1/(index+1)
                rr = {
                    'clone_SO': f'{unique_so_clone}',
                    'reciprocal_rank': reciprocal_rank,
                    'hit_number' : index + 1,
                    'oracle_clones_QA': [f'{clone[0].split("/")[-1]}_{clone[1]}_{clone[2]}' for clone in oracle_clones],
                    'siamese_clones_QA': [f'{clone[0].split("/")[-1]}_{clone[1]}_{clone[2]}' for clone in siamese_hit_attempts],
                    'relevants_clones_number': len(oracle_clones),
                    'attempts_number' : len(siamese_hit_attempts)
                    }
                break
            
            if (index + 1) == len(siamese_hit_attempts):
                reciprocal_rank += 0
                total_reciprocal_rank += 0
                rr = {
                    'clone_SO': f'{unique_so_clone}',
                    'reciprocal_rank': 0,
                    'hit_number' : 0,
                    'oracle_clones_QA': [f'{clone[0].split("/")[-1]}_{clone[1]}_{clone[2]}' for clone in oracle_clones],
                    'siamese_clones_QA': [f'{clone[0].split("/")[-1]}_{clone[1]}_{clone[2]}' for clone in siamese_hit_attempts],
                    'relevants_clones_number': len(oracle_clones),
                    'attempts_number' : len(siamese_hit_attempts)
                    }
                break


        rr['k_hits_correct'] = get_k_hits(siamese_hit_attempts, oracle_clones)

        for i in number_relevants_clones:
            if i <= len(oracle_clones):
                new_rr = add_precision_recall_apk(rr, siamese_hit_attempts, oracle_clones, i)
                copy_rr = copy.deepcopy(new_rr)
                remove_precision_recall_apk(rr, i)
                try:
                    all_reciprocal_rank[f'results_k@{i}'].append(copy_rr)
                except:
                    all_reciprocal_rank[f'results_k@{i}'] = []
                    all_reciprocal_rank[f'results_k@{i}'].append(copy_rr)

        try:
            attempts = len(siamese_hit_attempts)
            all_reciprocal_rank['siamese_status'][f'number_attempts_{attempts}'] += 1
        except:
            all_reciprocal_rank['siamese_status'][f'number_attempts_{attempts}'] = 1

    for _, row in not_predicted_clones.iterrows():
        oracle_clone = f"{row['file1']}_{row['start1']}_{row['end1']}"
        oracle_clones = get_qualitas_clones_in_dataframe_by_so_clone(row, df_clones)
        
        rr = {
            'clone_SO': f'{oracle_clone}',
            'reciprocal_rank': 0,
            'hit_number' : None,
            'oracle_clones_QA': [f'{clone[0].split("/")[-1]}_{clone[1]}_{clone[2]}' for clone in oracle_clones],
            'siamese_clones_QA': [],
            'relevants_clones_number': len(oracle_clones),
            'attempts_number' : 0
            }

        for i in number_relevants_clones:
            if i <= len(oracle_clones):
                new_rr = add_precision_recall_apk(rr, siamese_hit_attempts, oracle_clones, i)
                copy_rr = copy.deepcopy(new_rr)
                remove_precision_recall_apk(rr, i)
                try:
                    all_reciprocal_rank[f'results_k@{i}'].append(copy_rr)
                except:
                    all_reciprocal_rank[f'results_k@{i}'] = []
                    all_reciprocal_rank[f'results_k@{i}'].append(copy_rr)
        
            
    for k in number_relevants_clones:
        calculate_hit_number(all_reciprocal_rank, k)


    result_siamese_csv = result_siamese_csv.replace('.csv', '')
    
    mrr = total_reciprocal_rank/num_queries
    all_reciprocal_rank[f'mrr'] = '{:.3}'.format(mrr)

    for k in number_relevants_clones:
        mapk_result = 0
        if f'results_k@{k}' in all_reciprocal_rank: 
            for rr in all_reciprocal_rank[f'results_k@{k}']:
                mapk_result += rr[f'APK@{k}']

            all_reciprocal_rank[f'status@{k}']['queries@k'] = len(all_reciprocal_rank[f'results_k@{k}'])
            
            if mapk_result == 0:
                all_reciprocal_rank[f'MAP@{k}'] = mapk_result
                break 

            all_reciprocal_rank[f'MAP@{k}'] = '{:.3}'.format(mapk_result/len(all_reciprocal_rank[f'results_k@{k}']))
            

            if 'hit_None' in all_reciprocal_rank[f'status@{k}']:
                number_hit_none = all_reciprocal_rank[f'status@{k}']['hit_None']
                precision_queries = len(all_reciprocal_rank[f'results_k@{k}']) - number_hit_none 
                
                all_reciprocal_rank[f'status@{k}']['queries@k'] = precision_queries
                all_reciprocal_rank[f'MAP@{k}'] =  '{:.3}'.format(mapk_result/precision_queries)
                 

    with open(f'./result_metrics/{result_siamese_csv}.json', "w") as json_file:
        json.dump(all_reciprocal_rank, json_file, indent=4)
    return mrr, all_reciprocal_rank

def get_metrics():
    df_clones = pd.read_csv('NEW_clones_only_QS_EX_UD.csv')
    df_clones = filter_oracle(df_clones)
    get_problemns_in_oracle(df_clones)
    optimization_algorithms = ['bayesian_search']
    open('error_siamese_execution.txt', 'w').write('')

    for algorithm in optimization_algorithms:
        directory = f'output_{algorithm} copy'
        results_siamese_csv = get_files_in_folder(directory)

        mrr_by_siamese_result = {}
        results_by_algorithm = []

        all_result_time = find_lines_with_specific_text(f'./{algorithm}_result_time copy.txt', 'Runtime:')
        for index, result_siamese_csv in enumerate(results_siamese_csv):
            if result_siamese_csv == 'README.md':
                continue

            try:
                df_siamese = format_siamese_output(directory, result_siamese_csv)
                mrr_result, all_rr = calculate_metrics(result_siamese_csv, df_siamese, df_clones)
                mrr_by_siamese_result[result_siamese_csv] = mrr_result 
            except Exception as inst:
                print(inst)
                open('error_siamese_execution.txt', 'a').write(f'{result_siamese_csv}\n')
                print(f'error in {result_siamese_csv}')
                continue

            params_str = result_siamese_csv.replace('.csv', '').split('_')
            params = [param for i_,param in enumerate(params_str) if i_ % 2]
            
            result_row = [index+1,
                   result_siamese_csv,
                   *params,
                   all_result_time[index],
                   '{:.3}'.format(mrr_result),
                   ]

            for k in k_s:
                try:
                    result_row.append(all_rr[f'MAP@{k}'])
                except:
                    result_row.append(0)
        
            results_by_algorithm.append(result_row)

            df_metric = pd.DataFrame(results_by_algorithm, columns=columns)
            df_metric.loc[len(df_metric)] = [None for _ in range(len(columns))]
            
            try:
                df_metric.to_excel(f'results_{algorithm}.xlsx', index=False)
            except:
                print(index)
        
        df_metric = pd.DataFrame(results_by_algorithm, columns=columns)
        df_metric.loc[len(df_metric)] = [None for _ in range(len(columns))]
        
    return df_metric

columns = ['index',
        'filename',
        'cloneSize',
        'ngramSize',
        'QRPercentileNorm',
        'QRPercentileT2',
        'QRPercentileT1',
        'QRPercentileOrig',
        'normBoost',
        'T2Boost',
        'T1Boost',
        'origBoost',
        'simThreshold',
        'time',
        'mrr']

k_s = [1,2,3,4,5,6,7,8,24,26]
for k in k_s:
    columns.append(f'MAP@{k}')

results = {}
df_result = pd.DataFrame()


