from siamese_search import execute_siamese_search
from files_operations import most_recent_file, delete_files_in_folder
import time
import random

all_combinations = []
algorithm = 'random_search'

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
    parms['algorithm'] = algorithm
    execute_siamese_search(**parms)

def generate_unique_combination():
    while True:
        combination = generate_combination()
        if combination not in all_combinations:
            return combination

def generate_combination():
    boost = [-1, 1, 4, 10]
    combination=[random.randint(4, 24),
                random.randint(6, 10),
                random.randint(1, 20),
                random.choice(boost)]

    return combination        

def execute_random_search():
    print('NOTE: FIRST YOU NEED RUN kill_all_elasticserach.py')

    start_total_time = time.time()
    finish_time = 2 * 3600 + 35 * 60 # 2H + 35 min

    delete_files_in_folder(f'./output_{algorithm}')
    open(f'{algorithm}_result_time.txt', 'w').write('')

    i = 0
    while True:
        i += 1
        start_time = time.time()
        combination = generate_unique_combination()
        all_combinations.append(combination)

        print(f"Count {i}")
        print(f"Combination {combination}")
        evaluate_tool(combination)

        end_time = time.time()
        execution_time = (end_time - start_time) / 60
        print("Runtime to date: %.2f minutes" % execution_time)
        open(f'{algorithm}_result_time.txt', 'a').write(f"{combination}\nRuntime to date: %.2f minutes\n" % execution_time)

        total_execution_time = end_time - start_total_time
        if finish_time <= total_execution_time:
            break

    total_execution_time = (end_time - start_total_time) / 60
    print("Total execution time: %.2f minutes" % total_execution_time)
    open(f'{algorithm}_result_time.txt', 'a').write("Total execution time: %.2f minutes" % total_execution_time)

