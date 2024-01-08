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

def execute_siamese_index_properties(project, combinations):
    for combination in combinations:
        r1 = combination[0]
        r2 = combination[1]
        r3 = combination[2]
        
        destination_file = './n-gram-properties'
        config = open('index-config.properties', 'r').read()
        config = config.replace('t1NgramSize=4', f't1NgramSize={r1}')
        config = config.replace('t2NgramSize=4', f't2NgramSize={r2}')
        config = config.replace('ngramSize=4', f'ngramSize={r3}')
        config = config.replace('index=qualitas_corpus_complete', f'index=qualitas_corpus_r1-{r1}_r2-{r2}_r3-{r3}')
        new_config = f'{destination_file}/r1-{r1}_r2-{r2}_r3-{r3}.properties'
        open(new_config, 'w').write(config)
        command = f'cd Siamese-main && java -jar siamese-0.0.6-SNAPSHOT.jar -c index -i ./my_index/{project}/ -cf ../{new_config}'
        process = subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        process.wait()


r1 = set(range(4, 25))
r2 = set(range(4, 25))
r3 = set(range(4, 25))

combinations = list(product(r1, r2, r3))
project = 'qualitas_corpus_complete'
complete_path = '/home/denis/Hyperparameter-Optimization-Siamese/n-gram-properties'
for combination in combinations:
    r1 = combination[0]
    r2 = combination[1]
    r3 = combination[2]
    
    destination_file = './n-gram-properties'
    config = open('index-config.properties', 'r').read()
    config = config.replace('t1NgramSize=4', f't1NgramSize={r1}')
    config = config.replace('t2NgramSize=4', f't2NgramSize={r2}')
    config = config.replace('ngramSize=4', f'ngramSize={r3}')
    config = config.replace('index=qualitas_corpus_complete', f'index=qualitas_corpus_r1-{r1}_r2-{r2}_r3-{r3}')
    config_name = f'r1-{r1}_r2-{r2}_r3-{r3}.properties'
    new_config = f'{destination_file}/{config_name}'
    open(new_config, 'w').write(config)
    command = f'cd Siamese-main && java -jar siamese-0.0.6-SNAPSHOT.jar -c index -i ./my_index/{project}/ -cf ../{destination_file}/{config_name}'
    process = subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    process.wait()
    return_code = process.returncode
    
threads = []
for combination in combinations:
    thread = threading.Thread(target=execute_index_siamese, args=(combination,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

batch_size = 2
threads = []
for i in range(0, len(combinations), batch_size):
    batch_combinations = combinations[i:i+batch_size]
    batch_threads = []
    for combination in batch_combinations:
        thread = threading.Thread(target=execute_siamese_index_properties, args=(combination,))
        thread.start()
        batch_threads.append(thread)
        
    for thread in batch_threads:
        thread.join()
    threads.extend(batch_threads)

for thread in threads:
    thread.join()
