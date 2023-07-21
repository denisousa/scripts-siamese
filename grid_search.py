from siamese_search import execute_siamese_search
from itertools import product
import time


def format_dimension(parms):
    return {'ngramSize' : parms[0],
            'minCloneSize' : parms[1],
            'QRPercentile' : parms[2], 
            'Boost': parms[3]}

def evaluate_tool(parms):
    parms = format_dimension(parms)
    parms['config_folder'] = 'configurations_grid_search'
    parms['output_folder'] = 'output_grid_search'
    execute_siamese_search(**parms)

dimensions=[[4, 8, 16], # ngram
            [6, 10], # minCloneSize
            [2, 8, 10], # 
            [-1, 10]] # boosting


print('NOTE: FIRST YOU NEED RUN kill_all_elasticserach.py')
check = []
combinations = product(*dimensions)

start_total_time = time.time()
for i, combination in enumerate(combinations):
    start_time = time.time()
    text = f'{combination}'
    print(f"Count {i}")
    print(f"Combination {combination}")
    evaluate_tool(combination)

    end_time = time.time()
    execution_time = (end_time - start_time) / 60
    print("Runtime to date: %.2f minutes" % execution_time)
    open('result_time.txt', 'a').write(f"{combination}\nRuntime to date: %.2f minutes\n" % execution_time)

total_execution_time = (end_time - start_total_time) / 60
print("Total execution time: %.2f minutes" % total_execution_time)

