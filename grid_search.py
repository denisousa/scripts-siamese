from siamese_search import execute_siamese_search
from itertools import product
import json
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

dimensions=[[4, 24],
            [6, 10],
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

check = []
combinations = product(*dimensions)
# len_combinations = 20*4*20*20*20*20*4*4*4*4 # 3276800000

combination = [4,6,10,10,10,10,4,4,4,1]
evaluate_tool(combination)

count = 0
for i, combination in enumerate(combinations):
    count += 1
    print(f"Count {i}")
    print(f"Combination {combination}")
    evaluate_tool(combination)


'''best_parms = max(check, key=lambda x: x["f1_score"])

print("Melhores hiperparâmetros encontrados:")
print("parms:", best_parms)

with open("grid_searh_results.json", "w") as file:
    json.dump(check, file, indent=4)'''

end_time = time.time()
execution_time = (end_time - start_time) / 60

print("Tempo de execução: %.2f minutos" % execution_time)