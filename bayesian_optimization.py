'''
NOTE: Only Works with pip install "numpy<1.24.0"
'''

import pandas as pd
from siamese_operations import format_siamese_output
from oracle_operations import filter_oracle
from skopt import gp_minimize
from skopt.space import Integer, Categorical
from skopt.utils import use_named_args
from siamese_search import execute_siamese_search
from generate_metrics import calculate_mrr_and_rr
from datetime import datetime, timedelta
from files_operations import most_recent_file
import shutil
import sys
import os
from random import uniform

ngram = [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
minclonesize = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
qrpercentile = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
boost = [-1, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
simthreshold = [
    '10%,20%,30%,40%',
    '20%,30%,40%,50%',
    '30%,40%,50%,60%',
    '40%,50%,60%,70%',
    '50%,60%,70%,80%',
    '60%,70%,80%,90%',
    '10%,30%,40%,50%',
    '20%,40%,60%,70%',
    '30%,60%,80%,90%',
]

dimensions=[Categorical(ngram, name='ngramSize'),
            Integer(6, 16, name='minCloneSize'),
            Integer(2, 20, name='QRPercentileNorm'),
            Integer(2, 20, name='QRPercentileT2'),
            Integer(2, 20, name='QRPercentileT1'),
            Integer(2, 20, name='QRPercentileOrig'),
            Categorical(boost, name='normBoost'),
            Categorical(boost, name='t2Boost'),
            Categorical(boost, name='t1Boost'),
            Categorical(boost, name='origBoost'),
            Categorical(simthreshold, name='simThreshold')]


@use_named_args(dimensions)
def evaluate_tool(**parms):
    i = int(len(os.listdir(directory))) + 1

    print(f"Count {i}")
    print(f"Combination {parms}")
    parms_list = list(parms.values())

    file_exec = f'nS_{parms_list[0]}_cS_{parms_list[1]}_qrN_{parms_list[2]}_qrT2_{parms_list[3]}_qrT1_{parms_list[4]}_qrO_{parms_list[5]}_boN_{parms_list[6]}_boT2_{parms_list[7]}_boT1_{parms_list[8]}_boOr_{parms_list[9]}_simT_{parms_list[10]}'

    if parms_list in grid_search_results:
        filename = [filename for filename in os.listdir(f'output_grid_search') if file_exec in filename][0]
        shutil.copy(f'output_grid_search/{filename}', f'output_bayesian_search/{filename}')
        os.rename(f'{directory}/{most_recent_siamese_output}', f'{directory}/{i}_{most_recent_siamese_output}')
        
        index = grid_search_results.index(parms_list)
        mapk1 = df_grid_search_results.loc[index, "mrr"]
        loss = float(mapk1) * -1
        return loss
    

    if parms_list in random_search_results:
        filename = [filename for filename in os.listdir(f'output_grid_search') if file_exec in filename][0]
        shutil.copy(f'output_grid_search/{filename}', f'output_bayesian_search/{filename}')
        os.rename(f'{directory}/{most_recent_siamese_output}', f'{directory}/{i}_{most_recent_siamese_output}')

        index = random_search_results.index(parms_list)
        mapk1 = df_random_search_results.loc[index, "mrr"]
        loss = float(mapk1) * -1
        return loss
    
    
    parms['algorithm'] = algorithm
 
    start_time = datetime.now()
    execute_siamese_search(**parms)
    end_time = datetime.now()
    exec_time = end_time - start_time
    total_execution_time = end_time - start_total_time


    print(f"Runtime: {exec_time}")
    open(f'{algorithm}_result_time.txt', 'a').write(f'Success execution ')
    open(f'{algorithm}_result_time.txt', 'a').write( f'{list(parms.values())} \nRuntime: {exec_time}\n\n')

    most_recent_siamese_output, _ = most_recent_file(directory)
    df_siamese = format_siamese_output(directory, most_recent_siamese_output)
    all_rr = calculate_mrr_and_rr(most_recent_siamese_output, df_siamese, df_clones)
    mrr = all_rr["MRR (Mean Reciprocal Rank)"]
    os.rename(f'{directory}/{most_recent_siamese_output}', f'{directory}/{i}_{most_recent_siamese_output}')
    
    loss = float(mrr) * -1

    if grid_search_time <= total_execution_time:
        print(f"Total execution time: {total_execution_time}")
        open(f'{algorithm}_result_time.txt', 'a').write(f"\nTotal execution time: {total_execution_time}\n")
        print(f'Last Result - mrr:{mrr} | parms: {list(parms.values())}')
        sys.exit()

    print(f'\n \n \n loss: {loss}\n \n \n')
    return loss


def execute_bayesian_search():
    all_combinations = 3380

    result = gp_minimize(evaluate_tool,
                         dimensions=dimensions,
                         n_calls=all_combinations,
                         random_state=42)
    
    print(f'FINAL RESULT: {result}')


columns_parms = ['cloneSize',
        'ngramSize',
        'QRPercentileNorm',
        'QRPercentileT2',
        'QRPercentileT1',
        'QRPercentileOrig',
        'normBoost',
        'T2Boost',
        'T1Boost',
        'origBoost',
        'simThreshold']

algorithm = 'bayesian_search'
directory = f'output_{algorithm}'
# grid_search_time = timedelta(days=2, hours=6, minutes=10, seconds=49)
grid_search_time = timedelta(days=0, hours=3, minutes=10, seconds=49)
start_total_time = datetime.now()
df_clones = pd.read_csv('NEW_clones_only_QS_EX_UD.csv')
df_grid_search_results = pd.read_excel('result_grid_search.xlsx')
grid_search_results = df_grid_search_results[columns_parms].values.tolist()
df_random_search_results = pd.read_excel('result_random_search.xlsx')
random_search_results = df_random_search_results[columns_parms].values.tolist()
df_clones = filter_oracle(df_clones)
execute_bayesian_search()