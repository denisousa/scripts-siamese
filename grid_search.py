from siamese_search import execute_siamese_search
from itertools import product
import time


def format_dimension(parms):
    return {'ngramSize' : parms[0],
            'minCloneSize' : parms[1],
            'QRPercentileNorm' : parms[2], 
            'QRPercentileT2' : parms[3],
            'QRPercentileT1' : parms[4],
            'QRPercentileOrig' : parms[5],
            'normBoost': parms[6],
            't2Boost': parms[7],
            't1Boost': parms[8],
            'origBoost': parms[9]}


def evaluate_tool(parms):
    parms = format_dimension(parms)
    parms['config_folder'] = 'configurations_grid_search'
    parms['output_folder'] = 'output_grid_search'
    execute_siamese_search(**parms)

dimensions=[[24, 4],
            [10, 6],
            [1, 20],
            [1, 20],
            [1, 20],
            [1, 20],
            [-1, 10],
            [-1, 10],
            [-1, 10],
            [-1, 10]]

# 6 pontos
'''dimensions=[[4, 6, 8, 10, 12, 14],
            [6, 7, 8, 9, 10],
            [1, 4, 8, 12, 16, 20],
            [1, 4, 8, 12, 16, 20],
            [1, 4, 8, 12, 16, 20],
            [1, 4, 8, 12, 16, 20],
            [-1, 1, 4, 10],
            [-1, 1, 4, 10],
            [-1, 1, 4, 10],
            [-1, 1, 4, 10]]
'''
start_time = time.time()
print('FOR THIS SCRIPT WORS YOU NEED RUN kill_all_elasticserach.py')
print('AFTER YOU NEED RUN start_all_elasticserach.py')
print('THEN WAIT 2 MINUTEs')
#kill_all_clusters()

check = []
combinations = product(*dimensions)
# len_combinations = 20*4*20*20*20*20*4*4*4*4 # 3276800000

count = 0
for i, combination in enumerate(combinations):
    count += 1
    print(f"Count {i}")
    print(f"Combination {combination}")
    evaluate_tool(combination)

    end_time = time.time()
    execution_time = (end_time - start_time) / 60
    print("Tempo de execução até o presente momento: %.2f minutos" % execution_time)

print("Tempo de execução total: %.2f minutos" % execution_time)

