'''
Indexing
r1, r2, and r3 starting from 4 to 24 (step of 4) - Siamese Research
r1, r2, and r3 starting from 4 to 24 (step of 1 or 2) - Denis Research

Search
The query reduction thresholds should be somewhere around 1-15%

'''
import os
import gc
import subprocess
import threading
from elasticsearch_operations import execute_cluster_elasticserach, stop_cluster_elasticserach, create_clusters_elasticserach, create_one_cluster_elasticserach

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

def execute_siamese_index_properties(ngram):
    gc.collect()
    os.system('sync')
    stop_cluster_elasticserach(ngram) 
    execute_cluster_elasticserach(ngram)

    project = 'qualitas_corpus_clean'
    n_gram_properties_path = './n-gram-properties'
    elasticsearch_path = '/home/denis/programming/siamese-optmization/elasticsearch-siamese'
    elasticsearch_path = f'{elasticsearch_path}/elasticsearch-ngram-{ngram}'

    config = open('index-config.properties', 'r').read()
    config = config.replace('elasticsearchLoc=elasticsearchLoc', f'elasticsearchLoc={elasticsearch_path}')
    config = config.replace('cluster=cluster', f'cluster=stackoverflow')
    config = config.replace('t1NgramSize=4', f't1NgramSize={ngram}')
    config = config.replace('t2NgramSize=4', f't2NgramSize={ngram}')
    config = config.replace('ngramSize=4', f'ngramSize={ngram}')
    index_name = f'qualitas_corpus_n_gram_{ngram}'
    config = config.replace('index=qualitas_corpus_clean', f'index={index_name}')
    print(f'CONFIG NAME: {index_name} \n\n')
    new_config = f'{n_gram_properties_path}/n_gram_{ngram}.properties'
    open(new_config, 'w').write(config)
    command = f'java -jar siamese-0.0.6-SNAPSHOT.jar -c index -i ../siamese-optmization/Siamese/my_index/{project} -cf {new_config}'
    process = subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    process.wait()

    stop_cluster_elasticserach(ngram) 


print('FOR THIS SCRIPT WORS YOU NEED RUN kill_all_elasticserach.py')
#create_one_cluster_elasticserach(24,9220)
clusters = range(5,24)
for i in clusters:
    execute_siamese_index_properties(i)
#single_execution()
#multiple_execution()

