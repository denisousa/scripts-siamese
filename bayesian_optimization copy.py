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
from generate_metrics import calculate_metrics
from datetime import datetime, timedelta
from files_operations import most_recent_file
import sys
import time

dimensions=[Integer(4, 8, name='ngramSize'),
            Integer(6, 10, name='minCloneSize'),
            Integer(4, 10, name='QRPercentile'),
            Integer(4, 10, name='QRPercentileT2'),
            Integer(4, 10, name='QRPercentileT1'),
            Integer(4, 10, name='QRPercentileOrig'),
            Categorical([-1, 1, 4, 6, 10], name='normBoost'),
            Categorical([-1, 1, 4, 6, 10], name='T2Boost'),
            Categorical([-1, 1, 4, 6, 10], name='T1Boost'),
            Categorical([-1, 1, 4, 6, 10], name='origBoost'),
            Categorical(['30%,50%,70%,90%', '20%,40%,60%,80%'], name='simThreshold')]

@use_named_args(dimensions)
def evaluate_tool(**parms):
    i =+ 1

    print(f"Count {i}")
    print(f"Combination {parms}")
    parms['algorithm'] = algorithm
 
    start_time = time.time()
    execute_siamese_search(**parms)
    end_time = time.time()
    exec_time = end_time - start_time
    total_execution_time = end_time - start_total_time


    print(f"Runtime: {exec_time}")
    open(f'{algorithm}_result_time.txt', 'a').write(f'Success execution ')
    open(f'{algorithm}_result_time.txt', 'a').write( f'{parms} \nRuntime: {exec_time}\n\n')

    most_recent_siamese_output = most_recent_file(directory)
    df_siamese = format_siamese_output(directory, most_recent_siamese_output)
    mrr, all_rr = calculate_metrics(most_recent_siamese_output, df_siamese, df_clones)

    execution_time = (end_time - start_time) / 60
    print("Runtime to date: %.2f minutes" % execution_time)
    open(f'{algorithm}_result_time.txt', 'a').write(f"{parms}\nRuntime to date: %.2f minutes\n" % execution_time)

    loss = -mrr

    if grid_search_time <= total_execution_time:
        print(f"Total execution time: {total_execution_time}")
        open(f'{algorithm}_result_time.txt', 'a').write(f"\nTotal execution time: {total_execution_time}\n")
        print(f'Last Result - mrr:{mrr} | parms: {parms}')
        sys.exit()

    return loss


def execute_bayesian_search():
    all_combinations = 25920000

    result = gp_minimize(evaluate_tool,
                         dimensions=dimensions,
                         n_calls=all_combinations,
                         random_state=42)

algorithm = 'bayesian_search'
directory = f'output_{algorithm}'
grid_search_time = timedelta(days=2, hours=6, minutes=10, seconds=49)
start_total_time = datetime.now()
df_clones = pd.read_csv('NEW_clones_only_QS_EX_UD.csv')
df_clones = filter_oracle(df_clones)