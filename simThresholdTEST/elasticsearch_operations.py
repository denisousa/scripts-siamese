import re
import os
import subprocess
from time import sleep

def get_ngram_by_port():
    ngram_by_port = {}
    for ngram_i, port in zip(range(4,25), range(9200,9221)):
        ngram_by_port[ngram_i] = port
    return ngram_by_port

def create_one_cluster_elasticserach(ngram, port):
    elasticsearch_path = '../../siamese-optmization/elasticsearch-siamese'
    command_unzip = f'tar -xvf elasticsearch-2.2.0.tar.gz -C {elasticsearch_path}'
    command_rename = f'mv {elasticsearch_path}/elasticsearch-2.2.0 {elasticsearch_path}/elasticsearch-ngram-{ngram}'
    elasticsearch_yml_path = f'{elasticsearch_path}/elasticsearch-ngram-{ngram}/config/elasticsearch.yml'
    elasticsearch_yml_content = f'cluster.name: stackoverflow \nindex.query.bool.max_clause_count: 4096 \nhttp.port: {port}'

    os.system(command_unzip)
    sleep(1)

    os.system(command_rename)
    open(elasticsearch_yml_path, 'w').write(elasticsearch_yml_content)
    print(f'\nCREATE ELASTICSEARCH elasticsearch-ngram-{ngram}\n')

def create_clusters_elasticserach():
    elasticsearch_path = '../../siamese-optmization/elasticsearch-siamese'
    clusters = [5,7,9,11,13,15,17,19,21,23]
    for ngram_i in clusters:
        port = 9000 + ngram_i
        shards = 4
        replicas = 1
        shards_per_node = 2
        mem = 2

        command_unzip = f'tar -xvf elasticsearch-2.2.0.tar.gz -C {elasticsearch_path}'
        command_rename = f'mv {elasticsearch_path}/elasticsearch-2.2.0 {elasticsearch_path}/elasticsearch-ngram-{ngram_i}'
        elasticsearch_yml_path = f'{elasticsearch_path}/elasticsearch-ngram-{ngram_i}/config/elasticsearch.yml'
        elasticsearch_yml_content = f'cluster.name: stackoverflow \nindex.query.bool.max_clause_count: 8192 \nhttp.port: {port}'
        #elasticsearch_yml_content = f'{elasticsearch_yml_content}\nindex.number_of_shards: {shards}\nindex.number_of_replicas: {replicas}'
        #elasticsearch_yml_content = f'{elasticsearch_yml_content}\ncluster.routing.allocation.total_shards_per_node: {shards_per_node}'
        elasticsearch_yml_content = f'{elasticsearch_yml_content}\nindices.cache.filter.size: 20%'
        os.system(command_unzip)
        sleep(1)

        os.system(command_rename)
        open(elasticsearch_yml_path, 'w').write(elasticsearch_yml_content)

        elasticsearch_in_bat_path = f'{elasticsearch_path}/elasticsearch-ngram-{ngram_i}/bin/elasticsearch.in.bat'
        elasticsearch_in_bat_text = open(elasticsearch_in_bat_path, 'r').read()
        elasticsearch_in_bat_text = elasticsearch_in_bat_text.replace('ES_MIN_MEM=256m', f'ES_MIN_MEM={mem}g')
        elasticsearch_in_bat_text = elasticsearch_in_bat_text.replace('ES_MAX_MEM=1g', f'ES_MAX_MEM={mem}g')

        elasticsearch_in_sh_path = f'{elasticsearch_path}/elasticsearch-ngram-{ngram_i}/bin/elasticsearch.in.sh'
        elasticsearch_in_sh_text = open(elasticsearch_in_sh_path, 'r').read()
        elasticsearch_in_sh_text = elasticsearch_in_sh_text.replace('ES_MIN_MEM=256m', f'ES_MIN_MEM={mem}g')
        elasticsearch_in_sh_text = elasticsearch_in_sh_text.replace('ES_MAX_MEM=1g', f'ES_MAX_MEM={mem}g')


        open(elasticsearch_in_bat_path, 'w').write(elasticsearch_in_bat_text)
        open(elasticsearch_in_sh_path, 'w').write(elasticsearch_in_sh_text)
        print(f'\nCREATE ELASTICSEARCH elasticsearch-ngram-{ngram_i}\n')

def execute_cluster_elasticserach(ngram):
    elasticsearch_path = '../../siamese-optmization/elasticsearch-siamese'
    command_execute = f'{elasticsearch_path}/elasticsearch-ngram-{ngram}/bin/elasticsearch -d'
    print(f'EXECUTING elasticsearch-ngram-{ngram}')
    process = subprocess.Popen(command_execute, shell=True)
    process.wait()
    sleep(7)
    #os.system(command_execute)
    #process = subprocess.Popen(command_execute, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    #process.wait()

def stop_cluster_elasticserach(ngram):
    port = 9000 + ngram
    command_stop = f'sudo kill $(sudo lsof -t -i :{port})'
    print(f'STOP elasticsearch-ngram-{ngram}')
    os.system(command_stop)

def change_cluster_name(ngram_size):
    command = f'sudo -S kill $(sudo lsof -t -i :9200)'
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=None, stderr=None, close_fds=True)
    process.wait()

    elasticsearch_yml_path = '../../siamese-optmization/elasticsearch-2.2.0/config/elasticsearch.yml'
    pattern = r"cluster\.name:\s*(.*?)\s*\n"
    elasticsearch_yml_text = open(elasticsearch_yml_path, 'r').read()
    cluster_name = re.search(pattern, elasticsearch_yml_text).group(1)
    elasticsearch_yml_text = elasticsearch_yml_text.replace(cluster_name, f'n_gram_{ngram_size}')
    elasticsearch_yml_text = elasticsearch_yml_text
    open(elasticsearch_yml_path, 'w').write(elasticsearch_yml_text)


    command = f'../../siamese-optmization/elasticsearch-2.2.0/bin/elasticsearch'
    process = subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    process.wait()
