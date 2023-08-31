from siamese_search import execute_siamese_search
import time
import re

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
            'QRPercentile' : parms[2], 
            'normBoost': parms[3],
            't2Boost': parms[4],
            't1Boost': parms[5],
            'origBoost': parms[6]}

def evaluate_tool(simThreshold, parms):
    parms = format_dimension(parms)
    parms['algorithm'] = 'grid_search'
    parms['simThreshold'] = simThreshold
    execute_siamese_search(**parms)

def execute_grid_search(simThreshold, combinations):
    algorithm = 'grid_search'

    start_total_time = time.time()
    for i, combination in enumerate(combinations):
        start_time = time.time()
        print(f"Count {i}")
        print(f"Combination {combination}")
        evaluate_tool(simThreshold, combination)

        end_time = time.time()
        execution_time = (end_time - start_time) / 60
        print("Runtime to date: %.2f minutes" % execution_time)
        open(f'{algorithm}_result_time.txt', 'a').write(f"{combination}\nRuntime to date: %.2f minutes\n" % execution_time)

    total_execution_time = (end_time - start_total_time) / 60
    print("Total execution time: %.2f minutes" % total_execution_time)
    open(f'{algorithm}_result_time.txt', 'a').write("Total execution time: %.2f minutes" % total_execution_time)


combinations = [
    [6, 4, 10, -1, 4, 4, 1],
    [10, 16, 10, 10, 10, -1, -1],
    [4, 6, 10, 1, 4, 4, -1], # 4076
]

simThreshold_values = [10,20,30,40,50,60,70,80,90]

print("SE QUER EXECUTAR O STACKOVERFLOW FILTERED OU CUT, ALTERE EM: siamese_search.py")

for simThreshold in simThreshold_values:
    execute_grid_search(simThreshold, combinations)