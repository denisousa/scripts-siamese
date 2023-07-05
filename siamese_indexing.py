'''
Indexing
r1, r2, and r3 starting from 4 to 24 (step of 4) - Siamese Research
r1, r2, and r3 starting from 4 to 24 (step of 1 or 2) - Denis Research

Search
The query reduction thresholds should be somewhere around 1-15%

'''

import subprocess
from itertools import product
import threading
import os
from siamese_operations import execute_index_siamese
import shutil

project = 'qualitas_corpus_clean'

def single_execution():
    for combination in combinations:
        execute_siamese_index_properties(combination)



def multiple_execution():
    batch_size = 2
    threads = []
    for i in range(0, len(combinations), batch_size):
        batch_combinations = combinations[i:i+batch_size]
        batch_threads = []
        for combination in batch_combinations:
            thread = threading.Thread(target=execute_siamese_index_properties, args=(combination, ))
            thread.start()
            batch_threads.append(thread)
            
        for thread in batch_threads:
            thread.join()
        threads.extend(batch_threads)

    for thread in threads:
        thread.join()

def execute_siamese_index_properties(combination):
    r1 = combination[0]
    r2 = combination[1]
    r3 = combination[2]
    
    destination_file = './n-gram-properties'
    config = open('index-config.properties', 'r').read()
    config = config.replace('t1NgramSize=4', f't1NgramSize={r1}')
    config = config.replace('t2NgramSize=4', f't2NgramSize={r2}')
    config = config.replace('ngramSize=4', f'ngramSize={r3}')
    config_name = f'qualitas_corpus_n_gram_{r1}'
    config = config.replace('index=qualitas_corpus_clean', f'index={config_name}')
    print(f'CONFIG NAME: {config_name} \n\n')
    new_config = f'{destination_file}/n_gram_{r1}.properties'
    open(new_config, 'w').write(config)
    command = f'cd Siamese-main && java -jar siamese-0.0.6-SNAPSHOT.jar -c index -i ./my_index/{project}/ -cf ../{new_config}'
    process = subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    process.wait()

combinations = [(i,i,i) for i in range(1,25)][14:18]
complete_path = '/home/denis/Hyperparameter-Optimization-Siamese/n-gram-properties'

single_execution()
# multiple_execution()

