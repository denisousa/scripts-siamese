import pandas as pd
from siamese_operations import format_siamese_output
from oracle_operations import filter_oracle
from parameters_operations import get_parameters_in_dict
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
    df_matched_rows = dataframe[
        (dataframe['file1'] == so_clone['file1']) &
        (dataframe['start1'] == so_clone['start1']) &
        (dataframe['end1'] == so_clone['end1'])]
    df_matched_rows = df_matched_rows[['file2', 'start2', 'end2']]
    df_matched_rows.reset_index(drop=True, inplace=True)
    return df_matched_rows.values.tolist()


def get_exact_clones_that_in_oracle(df_clones, df_siamese):
    so_clones_from_oracle = [f"{row['file1']}|{row['start1']}|{row['end1']}" for _, row in df_clones.iterrows()]
    so_clones_from_siamese = [f"{row['file1']}|{row['start1']}|{row['end1']}" for _, row in df_siamese.iterrows()]

    so_clones_from_oracle = list(set(so_clones_from_oracle))
    so_clones_from_siamese = list(set(so_clones_from_siamese))

    unique_clones = [clone for clone in so_clones_from_siamese if clone in so_clones_from_oracle]

    data = {'file1': list(map(lambda clone: clone.split('|')[0], unique_clones)),
            'start1': list(map(lambda clone: int(clone.split('|')[1]), unique_clones)),
            'end1': list(map(lambda clone: int(clone.split('|')[2]), unique_clones))}

    df = pd.DataFrame(data)
    return df.sort_values(by='file1')

def get_clones_that_not_in_oracle(df_clones, df_siamese):
    exact_predict_data = []
    inside_predict_data = []
    not_predict_data = []

    df_clones = df_clones.drop_duplicates(subset=['file1', 'start1', 'end1'])
    df_clones_Test = df_clones[df_clones['file1'].duplicated()]

    for _, test in df_clones_Test.iterrows():
        df = df_clones[df_clones['file1'] == test['file1']]
        for _, new_test in df.iterrows():
            print(new_test.tolist()[:3])
        print('--------------')
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

    df_inside_predict = pd.DataFrame(inside_predict_data).sort_values(by='file1')
    df_inside_predict = df_inside_predict.drop_duplicates(subset=['file1', 'start1', 'end1'])

    df_not_predict = pd.DataFrame(not_predict_data).sort_values(by='file1')
    

    print(df_exact_predict.shape, df_inside_predict.shape, df_not_predict.shape)
    print(df_exact_predict.shape[0] + df_inside_predict.shape[0], df_siamese.shape[0])

    df_concat_predict = pd.concat([df_exact_predict, df_inside_predict], ignore_index=True)
    
    print(df_concat_predict.shape, df_siamese.shape)
    df2 = df_concat_predict[df_concat_predict.duplicated()]
    
    df_concat_predict = df_concat_predict.drop_duplicates(subset=['file1', 'start1', 'end1'])

    print(df2)
    return df_concat_predict, df_exact_predict, df_inside_predict, df_not_predict


def get_clones_that_not_in_siamese(df_clones, df_siamese):
    so_clones_from_oracle = [f"{row['file1']}|{row['start1']}|{row['end1']}" for _, row in df_clones.iterrows()]
    so_clones_from_siamese = [f"{row['file1']}|{row['start1']}|{row['end1']}" for _, row in df_siamese.iterrows()]

    so_clones_from_oracle = list(set(so_clones_from_oracle))
    so_clones_from_siamese = list(set(so_clones_from_siamese))
    unique_clones = [clone for clone in so_clones_from_oracle if clone not in so_clones_from_siamese]

    data = {'file1': list(map(lambda clone: clone.split('|')[0], unique_clones)),
            'start1': list(map(lambda clone: int(clone.split('|')[1]), unique_clones)),
            'end1': list(map(lambda clone: int(clone.split('|')[2]), unique_clones))}

    df = pd.DataFrame(data)
    return df.sort_values(by='file1')


def format_reciprocal_rank_result(reciprocal_rank_result, k, v):
    reciprocal_rank_result['clones'].append(k)
    reciprocal_rank_result['reciprocal_rank'].append(v['reciprocal_rank'])
    reciprocal_rank_result['hit_number'].append(v['hit_number'])
    reciprocal_rank_result['attempts_number'].append(v['attempts_number'])
    return reciprocal_rank_result


def calculate_hit_number(all_reciprocal_rank):
    for rr in all_reciprocal_rank['results']:
        for k, v in rr.items():
            if v['hit_number'] == 0:
                continue
            try:
                all_reciprocal_rank['status'][f"hit_{v['hit_number']}"] += 1
            except:
                all_reciprocal_rank['status'][f"hit_{v['hit_number']}"] = 1

    return all_reciprocal_rank

def get_inside_clones(df1, df2):
    relax_clones_result = []

    for _, row in df1.iterrows():
        df2_clones = df2[df2['file1'] == row['file1']]
        start1_relax = row['start1']
        end1_relax = row['end1']

        for index, row_df2 in df2_clones.iterrows():
            if start1_relax <= row_df2['start1'] and end1_relax >= row_df2['end1']:
                relax_clones_result.append(row)
                break
    
    return pd.DataFrame(relax_clones_result)

def calculate_mrr(simThreshold, result_siamese_csv, df_siamese, df_clones):
    # File1 -> Stackoverflow 
    # File2 -> Qualitas Corpus

    total_reciprocal_rank = 0.0
    print(simThreshold, result_siamese_csv)
    clones_only_siamese = get_clones_that_not_in_oracle(df_clones, df_siamese)


    exact_clones_in_oracle = get_exact_clones_that_in_oracle(df_clones, df_siamese)
    not_predicted_clones = get_clones_that_not_in_siamese(df_clones, df_siamese)

    df_queries = df_clones.drop_duplicates(subset=['file1', 'start1', 'end1'])
    num_queries = df_queries.shape[0]

    oracle_clones_inside_siamese = get_inside_clones(clones_only_siamese, df_clones)
    clones_in_oracle = pd.concat([oracle_clones_inside_siamese, exact_clones_in_oracle], ignore_index=True)

    siamese_clones_inside_oracle = get_inside_clones(df_clones, clones_only_siamese)
    clones_in_oracle = pd.concat([siamese_clones_inside_oracle, clones_in_oracle], ignore_index=True)
    
    all_reciprocal_rank = {
        'results': [],
        'status': { 
            'num_queries': num_queries,
            'correct_predictions': clones_in_oracle.shape[0],
            'exact_clones': exact_clones_in_oracle.shape[0],
            'oracle_clones_inside_siamese': oracle_clones_inside_siamese.shape[0],
            'siamese_clones_inside_oracle': siamese_clones_inside_oracle.shape[0],
            'not_predict': not_predicted_clones.shape[0],
            'correct_predictions_percentage': round((clones_in_oracle.shape[0]/num_queries)*100, 1),
            'total_prediction_clones': 0,
            'wrong_prediction_clones': 0,
        }
    }

    all_reciprocal_rank['parameters'] = get_parameters_in_dict(result_siamese_csv)

    for _, row in clones_in_oracle.iterrows():
        reciprocal_rank = 0
        
        oracle_clone = f"{row['file1']}_{row['start1']}_{row['end1']}"

        oracle_clones = get_qualitas_clones_in_dataframe_by_so_clone(row, df_clones)
        siamese_hit_attempts = get_qualitas_clones_in_dataframe_by_so_clone(row, df_siamese)
        
        for index, siamese_hit in enumerate(siamese_hit_attempts):
            clone_is_correct = check_clone_is_correct(oracle_clones, siamese_hit)

            if clone_is_correct:
                reciprocal_rank += 1/(index+1)
                total_reciprocal_rank += 1/(index+1)
                break
            
            # This code is not necessary
            if (index + 1) == len(siamese_hit_attempts):
                reciprocal_rank += 1/(index+1)
                total_reciprocal_rank += 0
                break

        rr = {
                f'{oracle_clone}': {
                'reciprocal_rank': reciprocal_rank,
                'hit_number' : index + 1,
                'attempts_number' : len(siamese_hit_attempts)
                }
            }
        all_reciprocal_rank['results'].append(rr)
        all_reciprocal_rank['status']['total_prediction_clones'] += len(siamese_hit_attempts)

        try:
            attempts = len(siamese_hit_attempts)
            all_reciprocal_rank['status'][f'number_attempts_{attempts}'] += 1
        except:
            all_reciprocal_rank['status'][f'number_attempts_{attempts}'] = 1

        if len(siamese_hit_attempts) > 1:
            all_reciprocal_rank['status']['wrong_prediction_clones'] += len(siamese_hit_attempts) - 1

    for _, row in not_predicted_clones.iterrows():
        so_clone = f"{row['file1']}_{row['start1']}_{row['end1']}"
        rr = {
            f'{so_clone}': {
            'reciprocal_rank': 0,
            'hit_number' : 0,
            'attempts_number' : 0
            }
        }
        all_reciprocal_rank['results'].append(rr)

    all_reciprocal_rank = calculate_hit_number(all_reciprocal_rank)
    result_siamese_csv = result_siamese_csv.replace('.csv', '')
    mrr = total_reciprocal_rank/num_queries
    all_reciprocal_rank['status']['mrr'] = mrr

    with open(f'reciprocal_rank_{simThreshold}/{result_siamese_csv}.json', "w") as json_file:
        json.dump(all_reciprocal_rank, json_file, indent=4)
    return mrr

def calculate_one_mrr(directory, result_siamese_csv):
    df_siamese = format_siamese_output(directory, result_siamese_csv)
    df_clones = pd.read_csv('clones_only_QS_EX_UD.csv')
    df_clones = filter_oracle(df_clones)
    return calculate_mrr(df_siamese, df_clones)

def calculate_complete_mrr(simThreshold):
    df_clones = pd.read_csv('clones_only_QS_EX_UD.csv')
    df_clones = filter_oracle(df_clones)
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
            except:
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