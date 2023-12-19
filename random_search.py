from siamese_search import execute_siamese_search
from datetime import datetime, timedelta
from itertools import product
import re
import random

def remove_duplicates(original_list):
    tuple_list = [tuple(sublist) for sublist in original_list]
    unique_tuples = set(tuple_list)
    return [list(item) for item in unique_tuples] 

def generate_all_combinations(all_combinations):
    len_all_combinations = len(all_combinations)
    new_all_combinations = []
    
    while True:
        new_combination = generate_unique_combination(all_combinations)
        new_all_combinations.append(new_combination)
        all_combinations.append(new_combination)

        new_all_combinations = remove_duplicates(new_all_combinations)

        if len(new_all_combinations) > (len_all_combinations * 1.1):
            break   

    return new_all_combinations

def generate_unique_combination(all_combinations):
    while True:
        combination = generate_combination()
        if combination not in all_combinations:
            return combination

def generate_combination():
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

    combination=[random.choice(ngram), # ngram
                random.choice(minclonesize), # minCloneSize
                random.choice(qrpercentile), # QRPercentileNorm
                random.choice(qrpercentile), # QRPercentileT2
                random.choice(qrpercentile), # QRPercentileT1
                random.choice(qrpercentile), # QRPercentileOrig
                random.choice(boost), # normBoost
                random.choice(boost), # t2Boost
                random.choice(boost), # t1Boost
                random.choice(boost), # origBoost
                random.choice(simthreshold)] # simThreshold 

    return combination

def cofigure_text(text):
    text = text.replace('cloneSize-','')
    text = text.replace('ngramSize-','')
    text = text.replace('qrNorm-','')
    text = text.replace('normBoost-','')
    text = text.replace('t2Boost-','')
    text = text.replace('t1Boost-','')
    text = text.replace('origBoost-','')
    return text

def extract_numbers(text):
    pattern = r'-?\d+'
    numbers = re.findall(pattern, text)
    return numbers

def get_parameters_in_dict(text):
    numbers = [int(i) for i in extract_numbers(text)]
    return {
        "cloneSize": numbers[0],
        "ngramSize": numbers[1],
        "qrNorm": numbers[2],
        "normBoost": numbers[3],
        "t2Boost": numbers[4],
        "t1Boost": numbers[5],
        "origBoost": numbers[6],
    }

def get_parameters_in_list(text):
    numbers = [int(i) for i in extract_numbers(text)]
    return {
        "cloneSize": numbers[0],
        "ngramSize": numbers[1],
        "qrNorm": numbers[2],
        "normBoost": numbers[3],
        "t2Boost": numbers[4],
        "t1Boost": numbers[5],
        "origBoost": numbers[6],
    }

def get_combination(text):
    text = cofigure_text(text)
    return [int(i) for i in extract_numbers(text)]


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
    parms['algorithm'] = 'random_search'
    execute_siamese_search(**parms)

def execute_random_search(combinations):
    algorithm = 'random_search'

    # grid_search_time = timedelta(days=2, hours=6, minutes=10, seconds=49)
    grid_search_time = timedelta(days=0, hours=3, minutes=10, seconds=49)
    start_total_time = datetime.now()

    for i, combination in enumerate(combinations):
        i += 1

        start_time = datetime.now()
        print(f"\n\nCount {i}")
        print(f"Combination {combination}")
        evaluate_tool(combination)

        end_time = datetime.now()
        exec_time = end_time - start_time
        total_execution_time = end_time - start_total_time

        if grid_search_time < total_execution_time:
            break

        print(f"Runtime: {exec_time}")
        open(f'{algorithm}_result_time.txt', 'a').write(f'Success execution ')
        open(f'{algorithm}_result_time.txt', 'a').write( f'{combination} \nRuntime: {exec_time}\n\n')

    print(f"Total execution time: {total_execution_time}")
    open(f'{algorithm}_result_time.txt', 'a').write(f"\nTotal execution time: {total_execution_time}\n")


grid_search_params = [
    [6, 4, 8], # ngram
    [6, 10], # minCloneSize
    [8, 10], # QRPercentileNorm
    [8, 10], # QRPercentileT2
    [8, 10], # QRPercentileT1
    [8, 10], # QRPercentileOrig
    [-1, 10], # normBoost
    [-1, 10], # t2Boost
    [-1, 10], # t1Boost
    [-1, 10], # origBoost
    ['30%,50%,70%,90%','20%,40%,60%,80%'], # simThreshold 
]

combinations = list(product(*grid_search_params))

combinations = generate_all_combinations(combinations)
print(len(combinations))

execute_random_search(combinations)