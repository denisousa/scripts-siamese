from siamese_search import execute_siamese_search
from files_operations import delete_files_in_folder
from itertools import product
import time


def format_dimension(parms):
    return {'ngramSize' : parms[0],
            'minCloneSize' : parms[1],
            'QRPercentile' : parms[2], 
            'normBoost': parms[3],
            't2Boost': parms[4],
            't1Boost': parms[5],
            'origBoost': parms[6]}

def evaluate_tool(parms):
    parms = format_dimension(parms)
    parms['algorithm'] = 'grid_search'
    execute_siamese_search(**parms)

def execute_grid_search():
    dimensions=[[4],      #ngramSize
                [6],         #cloneSize
                [2],      #qrPercentile
                [4],  #boost
                [1],  #boost
                [4],  #boost
                [4]]  #boost

    print('NOTE: FIRST YOUS NEED RUN kill_all_elasticserach.py')
    combinations = product(*dimensions)

    algorithm = 'grid_search'
    # delete_files_in_folder(f'./output_{algorithm}')
    # open(f'{algorithm}_result_time.txt', 'w').write('')

    start_total_time = time.time()
    for i, combination in enumerate(combinations):
        start_time = time.time()
        print(f"Count {i}")
        print(f"Combination {combination}")
        evaluate_tool(combination)

        end_time = time.time()
        execution_time = (end_time - start_time) / 60
        print("Runtime to date: %.2f minutes" % execution_time)
        open(f'{algorithm}_result_time.txt', 'a').write(f"{combination}\nRuntime to date: %.2f minutes\n" % execution_time)

    total_execution_time = (end_time - start_total_time) / 60
    print("Total execution time: %.2f minutes" % total_execution_time)
    open(f'{algorithm}_result_time.txt', 'a').write("Total execution time: %.2f minutes" % total_execution_time)
