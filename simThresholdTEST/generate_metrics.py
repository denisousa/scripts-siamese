import pandas as pd
from siamese_operations import format_siamese_output
from oracle_operations import filter_oracle
from parameters_operations import get_parameters_in_dict
import copy
import json
import os
import re
import numpy as np

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
    precisions = [precision_at_k(recommended_items, relevant_items, i) for i in range(1, k)]
    
    if k == 1:
        precisions = [precision_at_k(recommended_items, relevant_items, i) for i in range(1, k+1)]
        
    return round(sum(precisions) / k, 2)


def mapk(recommended_items, relevant_items, k):
    return round(np.mean([apk(a,p,k) for a,p in zip(recommended_items, relevant_items)]),2)


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
        oracle_clone = {'file1': oracle_clone[0], 'start2': oracle_clone[1], 'end2': oracle_clone[2]}

        # Oracle inside Siamese
        start2_condition = oracle_clone['start2'] >= siamese_clone['start2']
        end2_condition = oracle_clone['end2'] <= siamese_clone['end2']

        if start2_condition and end2_condition:
            return True, list(oracle_clone.values())
            
        # Siamese inside Oracle
        start2_condition = oracle_clone['start2'] <= siamese_clone['start2']
        end2_condition = oracle_clone['end2'] >= siamese_clone['end2']

        if start2_condition and end2_condition:
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

    for rr in all_reciprocal_rank[f'results_k@{k}']:

        if rr['hit_number'] == 0:
            continue

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


def calculate_mrr(simThreshold, result_siamese_csv, df_siamese, df_clones):
    # File1 -> Stackoverflow 
    # File2 -> Qualitas Corpus

    total_reciprocal_rank = 0.0
    print(simThreshold, result_siamese_csv)
    
    so_clones = get_so_clones_from_oracle(df_clones, df_siamese)
    clones_in_oracle = so_clones['correct_predictions']
    not_predicted_clones = so_clones['not_predictions']
    exact_clones_in_oracle = so_clones['exact_predictions']
    inside_clones_in_oracle = so_clones['inside_predictions']
    exact_inside_prediciton = so_clones['exact_inside_predictions']
    
    df_queries = df_clones.drop_duplicates(subset=['file1', 'start1', 'end1'])
    num_queries = df_queries.shape[0]

    all_reciprocal_rank = {
        'status': { 
            'num_queries': num_queries,
            'correct_predictions': clones_in_oracle.shape[0],
            'not_predict': not_predicted_clones.shape[0],
        },
        'parameters': get_parameters_in_dict(result_siamese_csv),
        #'correct_predictions': clones_in_oracle[['file1', 'start1', 'end1']].values.tolist(),
        #'not_predictions': not_predicted_clones.values.tolist() 
    }

    relevants_clones = set()

    for _, row in clones_in_oracle.iterrows():
        reciprocal_rank = 0
        
        unique_so_clone = f"{row['file1']}_{row['start1']}_{row['end1']}"
        oracle_clones = get_qualitas_clones_in_dataframe_by_so_clone(row, df_clones)
        siamese_hit_attempts = get_qualitas_clones_in_dataframe_by_so_clone(row, df_siamese)
        
        for index, siamese_hit in enumerate(siamese_hit_attempts):
            clone_is_correct, oracle_clone_hit = check_clone_is_correct(oracle_clones, siamese_hit)

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
                    'reciprocal_rank': reciprocal_rank,
                    'hit_number' : 0,
                    'oracle_clones_QA': [f'{clone[0].split("/")[-1]}_{clone[1]}_{clone[2]}' for clone in oracle_clones],
                    'siamese_clones_QA': [f'{clone[0].split("/")[-1]}_{clone[1]}_{clone[2]}' for clone in siamese_hit_attempts],
                    'relevants_clones_number': len(oracle_clones),
                    'attempts_number' : len(siamese_hit_attempts)
                    }
                break

        
        number_relevants = rr['relevants_clones_number']
        relevants_clones.add(number_relevants)
        rr['k_hits_correct'] = get_k_hits(siamese_hit_attempts, oracle_clones)
        
        rr[f'Precision@{number_relevants}'] = precision_at_k(siamese_hit_attempts, oracle_clones, number_relevants)
        rr[f'Recall@{number_relevants}'] = recall_at_k(siamese_hit_attempts, oracle_clones, number_relevants)
        rr[f'APK@{number_relevants}'] = apk(siamese_hit_attempts, oracle_clones, number_relevants)
        
        try:
            all_reciprocal_rank[f'results_k@{number_relevants}'].append(rr)
        except:
            all_reciprocal_rank[f'results_k@{number_relevants}'] = []
            all_reciprocal_rank[f'results_k@{number_relevants}'].append(rr)
        
        try:
            attempts = len(siamese_hit_attempts)
            all_reciprocal_rank['status'][f'number_attempts_{attempts}'] += 1
        except:
            all_reciprocal_rank['status'][f'number_attempts_{attempts}'] = 1

        if len(siamese_hit_attempts) > 1:
            pass

    for _, row in not_predicted_clones.iterrows():
        oracle_clone = f"{row['file1']}_{row['start1']}_{row['end1']}"

        oracle_clones = get_qualitas_clones_in_dataframe_by_so_clone(row, df_clones)
        
        rr = {
            'clone_SO': f'{oracle_clone}',
            'reciprocal_rank': 0,
            'hit_number' : 0,
            'oracle_clones_QA': [f'{clone[0].split("/")[-1]}_{clone[1]}_{clone[2]}' for clone in oracle_clones],
            'siamese_clones_QA': [],
            'relevants_clones_number': len(oracle_clones),
            'attempts_number' : 0
            }

        rr[f'Precision@{number_relevants}'] = precision_at_k(siamese_hit_attempts, oracle_clones, number_relevants)
        rr[f'Recall@{number_relevants}'] = recall_at_k(siamese_hit_attempts, oracle_clones, number_relevants)
        rr[f'APK@{number_relevants}'] = apk(siamese_hit_attempts, oracle_clones, number_relevants)
        
        try:
            all_reciprocal_rank[f'results_k@{number_relevants}'].append(rr)
        except:
            all_reciprocal_rank[f'results_k@{number_relevants}'] = []
            all_reciprocal_rank[f'results_k@{number_relevants}'].append(rr)

    for relevant_k in list(relevants_clones):
        calculate_hit_number(all_reciprocal_rank, relevant_k)

    result_siamese_csv = result_siamese_csv.replace('.csv', '')
    
    mrr = total_reciprocal_rank/num_queries

    '''all_reciprocal_rank['status']['MAP@1'] = all_reciprocal_rank['status']['MAP@1']/num_queries
    all_reciprocal_rank['status']['MAP@3'] = all_reciprocal_rank['status']['MAP@3']/num_queries
    all_reciprocal_rank['status']['MAP@5'] = all_reciprocal_rank['status']['MAP@5']/num_queries'''
    
    for relevant_k in list(relevants_clones):
        mapk_result = 0
        for rr in all_reciprocal_rank[f'results_k@{relevant_k}']:
            mapk_result += rr[f'APK@{relevant_k}']
        
        all_reciprocal_rank[f'MAPK@{relevant_k}'] = mapk_result/num_queries

    with open(f'reciprocal_rank_{simThreshold}/{result_siamese_csv}.json', "w") as json_file:
        json.dump(all_reciprocal_rank, json_file, indent=4)
    return mrr

def calculate_one_mrr(directory, result_siamese_csv):
    df_siamese = format_siamese_output(directory, result_siamese_csv)
    df_clones = pd.read_csv('NEW_clones_only_QS_EX_UD.csv')
    df_clones = filter_oracle(df_clones)
    return calculate_mrr(df_siamese, df_clones)

def calculate_complete_mrr(simThreshold):
    df_clones = pd.read_csv('NEW_clones_only_QS_EX_UD.csv')
    df_clones = filter_oracle(df_clones)
    get_problemns_in_oracle(df_clones)
    # optimization_algorithms = ['grid_search', 'random_search', 'bayesian_search']
    optimization_algorithms = ['grid_search']
    columns = ['index',
               'filename',
               'cloneSize',
               'ngramSize',
               'qrNorm',
               'normBoost',
               'T2Boost',
               'T1Boost',
               'origBoost',
               #'time',
               'mrr']

    open('error_siamese_execution.txt', 'w').write('')

    for algorithm in optimization_algorithms:
        directory = f'output_{algorithm}_{simThreshold}'
        results_siamese_csv = get_files_in_folder(directory)

        if not os.path.exists(f'reciprocal_rank_{simThreshold}'):
            os.makedirs(f'reciprocal_rank_{simThreshold}')

        mrr_by_siamese_result = {}
        mrr_results_by_algorithm = []
        all_result_time = open(f'./{algorithm}_result_time.txt', 'r').read()
        result_time = list(map(float, find_float_numbers(all_result_time)))
        result_time = [round((int(str(time).replace('.',''))/60),2) for time in result_time]

        for index, result_siamese_csv in enumerate(results_siamese_csv):
            if result_siamese_csv == 'README.md':
                continue

            try:
                df_siamese = format_siamese_output(directory, result_siamese_csv)
                # df = pd.read_csv(f'./output_grid_search_{simThreshold}/{result_siamese_csv}')
                mrr_result = calculate_mrr(simThreshold, result_siamese_csv, df_siamese, df_clones)
                mrr_by_siamese_result[result_siamese_csv] = mrr_result
            except Exception as inst:
                print(inst)
                open('error_siamese_execution.txt', 'a').write(f'{result_siamese_csv}\n')
                print(f'error in {result_siamese_csv}')
                continue

            params = extract_text_between_hyphens_and_underscores(result_siamese_csv)
            params = [int(num) for num in params]
            
            mrr_result_row = [index+1]
            mrr_result_row.append(result_siamese_csv)
            for param in params:
                mrr_result_row.append(param)
            # mrr_result_row.append(result_time[index])
            mrr_result_row.append(mrr_result)

            mrr_results_by_algorithm.append(mrr_result_row)
        
        mrr_results_by_algorithm.append([None for _ in range(10)])
        df_metric = pd.DataFrame(mrr_results_by_algorithm, columns=columns)
  
    return df_metric

results = {}
df_result = pd.DataFrame()
simThreshold_list = [50,60,70,80,90]
for simThreshold in simThreshold_list:
    df_metrics = calculate_complete_mrr(simThreshold)
    df_metrics['simThreshold'] = f'{simThreshold}%,{simThreshold}%,{simThreshold}%,{simThreshold}%'
    df_result = pd.concat([df_result, df_metrics])
    df_result.at[df_result.index[-1], 'simThreshold'] = None


df_result.to_excel(f'mrr_result.xlsx', index=False)