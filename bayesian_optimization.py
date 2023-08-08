'''
NOTE: Only Works with pip install "numpy<1.24.0"
'''

from skopt import gp_minimize
from skopt.space import Integer, Categorical
from skopt.utils import use_named_args
from siamese_search import execute_siamese_search
from metric_mrr import calculate_one_mrr
from files_operations import most_recent_file, delete_files_in_folder
import sys
import time

dimensions=[Integer(4, 24, name='ngramSize'),
            Integer(6, 10, name='minCloneSize'),
            Integer(1, 20, name='QRPercentile'),
            Categorical([-1, 1, 4, 10], name='normBoost'),
            Categorical([-1, 1, 4, 10], name='T2Boost'),
            Categorical([-1, 1, 4, 10], name='T1Boost'),
            Categorical([-1, 1, 4, 10], name='origBoost')]

i = 0
start_total_time = time.time()
finish_time = 2 * 3600 + 35 * 60 # 2H + 35 min
algorithm = 'bayesian_search'

@use_named_args(dimensions)
def evaluate_tool(**parms):
    i =+ 1
    start_time = time.time()

    print(f"Count {i}")
    print(f"Combination {parms}")

    parms['algorithm'] = algorithm
    execute_siamese_search(**parms)
    directory_bayesian_results = f'output_{parms["algorithm"]}'
    most_recent_siamese_output = most_recent_file(directory_bayesian_results)
    mrr = calculate_one_mrr(directory_bayesian_results, most_recent_siamese_output)

    end_time = time.time()
    execution_time = (end_time - start_time) / 60
    print("Runtime to date: %.2f minutes" % execution_time)
    open(f'{algorithm}_result_time.txt', 'a').write(f"{parms}\nRuntime to date: %.2f minutes\n" % execution_time)

    loss = -mrr

    total_execution_time = end_time - start_total_time
    if finish_time <= total_execution_time:
        total_execution_time = (end_time - start_total_time) / 60
        print("Total execution time: %.2f minutes" % total_execution_time)
        open(f'{algorithm}_result_time.txt', 'a').write("Total execution time: %.2f minutes" % total_execution_time)
        sys.exit()

    return loss


def execute_bayesian_search():
    delete_files_in_folder(f'./output_{algorithm}')
    open(f'{algorithm}_result_time.txt', 'w').write('')

    result = gp_minimize(evaluate_tool, dimensions=dimensions, n_calls=1200, random_state=42)

