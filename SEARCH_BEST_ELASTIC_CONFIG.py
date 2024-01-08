from generate_metrics import get_metrics
from siamese_search import execute_siamese_search
from itertools import product
import pandas as pd
from datetime import datetime

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
            'origBoost': parms[9],
            'simThreshold': parms[10]}

def evaluate_tool(parms):
    parms = format_dimension(parms)
    parms['algorithm'] = 'grid_search'
    parms['output_folder'] = 'output_grid_search'
    execute_siamese_search(**parms)


param = [
    [4], # ngram
    [6, 10], # minCloneSize
    [8, 10], # QRPercentileNorm
    [8, 10], # QRPercentileT2
    [8, 10], # QRPercentileT1
    [8, 10], # QRPercentileOrig
    [-1, 10], # normBoost
    [-1, 10], # t2Boost
    [-1, 10], # t1Boost
    [-1, 10], # origBoost
    ['20%,40%,60%,80%', '30%,50%,70%,90%'], # simThreshold 
]
algorithm = 'grid_search'
current_datetime = datetime.now()

combinations = list(product(*param))[:3]
for combination in combinations:

    start_time = datetime.now()
    print(f"Combination {combination}")
    evaluate_tool(combination)

    end_time = datetime.now()
    exec_time = end_time - start_time

    result_time_path = f'time_record/{algorithm}/{current_datetime}.txt'
    print(f"Runtime: {exec_time}")
    open(result_time_path, 'a').write(f'Success execution ')
    open(result_time_path, 'a').write( f'{combination} \nRuntime: {exec_time}\n\n')


get_metrics([algorithm])

df = pd.read_excel('grid_search_result.xlsx')
print(df['time'])


'''
Não consegui fazer funcionar configurando por arquivo
Por arquivo só funcionou o número de shard
'''


# MUDANDO NUMERO DE SHARD
''' CASE 0 - 0 SHARDS
0    0:00:54.331843
1    0:00:55.660608
2    0:00:59.156795
'''

''' CASE 1 - 2 SHARDS
0    0:00:56.668729
1    0:00:58.027712
2    0:00:57.617909
'''

''' CASE 2 - 6 SHARDS
0    0:01:11.821715
1    0:01:08.962195
2    0:01:09.399567
'''