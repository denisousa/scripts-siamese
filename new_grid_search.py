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

def evaluate_tool(parms):
    parms = format_dimension(parms)
    parms['algorithm'] = 'grid_search'
    execute_siamese_search(**parms)

def execute_grid_search(combinations):
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


files = open('error_siamese_execution.txt', 'r').read().split('\n')
combinations = [get_combination(file_) for file_ in files]
execute_grid_search(combinations)