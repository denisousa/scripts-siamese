import re
import os
import subprocess
from time import sleep

def create_clusters_elasticserach():
    elasticsearch_path = '../siamese-optmization/elasticsearch-siamese'
    for ngram_i, port in zip(range(4,24), range(9200,9221)):
        command_unzip = f'tar -xvf elasticsearch-2.2.0.tar.gz -C {elasticsearch_path}'
        command_rename = f'mv {elasticsearch_path}/elasticsearch-2.2.0 {elasticsearch_path}/elasticsearch-ngram-{ngram_i}'
        elasticsearch_yml_path = f'{elasticsearch_path}/elasticsearch-ngram-{ngram_i}/config/elasticsearch.yml'
        elasticsearch_yml_content = f'cluster.name: cluster-ngram-{ngram_i} \nindex.query.bool.max_clause_count: 4096 \nhttp.port: {port}'

        os.system(command_unzip)
        os.system(command_rename)
        open(elasticsearch_yml_path, 'w').write(elasticsearch_yml_content)

def execute_cluster_elasticserach(ngram):
    elasticsearch_path = '../siamese-optmization/elasticsearch-siamese'
    command_execute = f'{elasticsearch_path}/elasticsearch-ngram-{ngram}/bin/elasticsearch -d'
    print(f'EXECUTING elasticsearch-ngram-{ngram} NOW')
    os.system(command_execute)
    sleep(6)
    #process = subprocess.Popen(command_execute, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    #process.wait()

def stop_cluster_elasticserach(ngram):
    for ngram_i, port in zip(range(4,24), range(9200,9221)):
        if ngram_i == ngram:
            command_stop = f'sudo kill $(sudo lsof -t -i :{port})'
            print(f'STOP elasticsearch-ngram-{ngram} NOW')
            os.system(command_stop)

def change_cluster_name(ngram_size):
    command = f'sudo -S kill $(sudo lsof -t -i :9200)'
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=None, stderr=None, close_fds=True)
    process.wait()

    elasticsearch_yml_path = '../siamese-optmization/elasticsearch-2.2.0/config/elasticsearch.yml'
    pattern = r"cluster\.name:\s*(.*?)\s*\n"
    elasticsearch_yml_text = open(elasticsearch_yml_path, 'r').read()
    cluster_name = re.search(pattern, elasticsearch_yml_text).group(1)
    elasticsearch_yml_text = elasticsearch_yml_text.replace(cluster_name, f'n_gram_{ngram_size}')
    open(elasticsearch_yml_path, 'w').write(elasticsearch_yml_text)

    command = f'../siamese-optmization/elasticsearch-2.2.0/bin/elasticsearch'
    process = subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    process.wait()
