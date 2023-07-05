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

project = 'qualitas_corpus_clean'

def execute_siamese_index_properties(combination):
    r1 = combination[0]
    r2 = combination[1]
    r3 = combination[2]
    
    destination_file = './n-gram-properties'
    config = open('index-config.properties', 'r').read()
    config = config.replace('t1NgramSize=4', f't1NgramSize={r1}')
    config = config.replace('t2NgramSize=4', f't2NgramSize={r2}')
    config = config.replace('ngramSize=4', f'ngramSize={r3}')
    index_name = f'qualitas_corpus_n_gram_{r1}'
    config = config.replace('index=qualitas_corpus_clean', f'index={index_name}')
    print(f'INDEX NAME: {index_name} \n\n')
    config_name = f'{destination_file}/n_gram_{r1}.properties'
    open(config_name, 'w').write(config)
    command = f'cd Siamese-main && java -jar siamese-0.0.6-SNAPSHOT.jar -c index -i ./my_index/{project}/ -cf ../{config_name}'
    process = subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    process.wait()

def execute_with_thread():
    batch_size = 2
    threads = []
    for i in range(4, 24, batch_size):
        batch_combinations = [(i+inc,i+inc,i+inc) for inc in range(batch_size)]
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


complete_path = '/home/denis/Hyperparameter-Optimization-Siamese/n-gram-properties'
execute_with_thread()
