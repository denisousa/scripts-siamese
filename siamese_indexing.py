'''
Indexing
r1, r2, and r3 starting from 4 to 24 (step of 4) - Siamese Research
r1, r2, and r3 starting from 4 to 24 (step of 1 or 2) - Denis Research

Search
The query reduction thresholds should be somewhere around 1-15%

'''

import subprocess
import threading
from elasticsearch_operations import execute_cluster_elasticserach, stop_cluster_elasticserach
from create_clusters import create_clusters_elasticserach

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
    ngram = 4

    stop_cluster_elasticserach(ngram) 
    execute_cluster_elasticserach(ngram)    

    project = 'qualitas_corpus_clean'
    n_gram_properties_path = './n-gram-properties'
    elasticsearch_path = '/home/denis/programming/siamese-optmization/elasticsearch-siamese'
    elasticsearch_path = f'{elasticsearch_path}/elasticsearch-ngram-{ngram}'

    config = open('index-config.properties', 'r').read()
    config = config.replace('elasticsearchLoc=elasticsearchLoc', f'elasticsearchLoc={elasticsearch_path}')
    config = config.replace('cluster=cluster', f'cluster=cluster-ngram-{ngram}')
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


#create_clusters_elasticserach()
combinations = [(i,i,i) for i in range(4,25)]
execute_siamese_index_properties(4)
#single_execution()
#multiple_execution()

