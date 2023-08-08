from elasticsearch_operations import execute_cluster_elasticserach, stop_cluster_elasticserach
from files_operations import most_recent_file
import subprocess
import os
import gc

def get_config_path(parms):
    clonesSize = f'cloneSize-{parms["minCloneSize"]}_'
    ngramSize = f'ngramSize-{parms["ngramSize"]}_'
    qrPercentile = f'qrNorm-{parms["QRPercentile"]}_'
    normBoost = f'normBoost-{parms["normBoost"]}_'
    t2Boost = f't2Boost-{parms["t2Boost"]}_'
    t1Boost = f't1Boost-{parms["t1Boost"]}_'
    origBoost = f'origBoost-{parms["origBoost"]}_'
    config_name = clonesSize + ngramSize + qrPercentile + normBoost + t2Boost + t1Boost + origBoost
    destination_file = f'./configurations_{parms["algorithm"]}'
    return f'{destination_file}/{config_name}.properties'

def generate_config_file(parms):
    elasticsearch_path = '/home/denis/programming/siamese-optmization/elasticsearch-siamese'
    elasticsearch_path = f'{elasticsearch_path}/elasticsearch-ngram-{parms["ngramSize"]}'

    config = open('search-config.properties', 'r').read()
    config = config.replace('elasticsearchLoc=elasticsearchLoc', f'elasticsearchLoc={elasticsearch_path}')
    config = config.replace('outputFolder=search_results', f'outputFolder=output_{parms["algorithm"]}')
    config = config.replace('cluster=cluster', f'cluster=stackoverflow')
    config = config.replace('ngramSize=4', f'ngramSize={parms["ngramSize"]}')
    config = config.replace('t2NgramSize=4', f't2NgramSize={parms["ngramSize"]}')
    config = config.replace('t1NgramSize=4', f't1NgramSize={parms["ngramSize"]}')
    config = config.replace('minCloneSize=6', f'minCloneSize={parms["minCloneSize"]}')
    config = config.replace('QRPercentileNorm=10', f'QRPercentileNorm={parms["QRPercentile"]}')
    config = config.replace('QRPercentileT2=10', f'QRPercentileT2={parms["QRPercentile"]}')
    config = config.replace('QRPercentileT1=10', f'QRPercentileT1={parms["QRPercentile"]}')
    config = config.replace('QRPercentileOrig=10', f'QRPercentileOrig={parms["QRPercentile"]}')
    config = config.replace('normBoost=4', f'normBoost={parms["normBoost"]}')
    config = config.replace('t2Boost=4', f't2Boost={parms["t2Boost"]}')
    config = config.replace('t1Boost=4', f't1Boost={parms["t1Boost"]}')
    config = config.replace('origBoost=1', f'origBoost={parms["origBoost"]}')
    config = config.replace('qualitas_corpus_clean', f'qualitas_corpus_n_gram_{parms["ngramSize"]}')
    
    properties_path = get_config_path(parms)
    open(properties_path, 'w').write(config)
    return properties_path

def execute_siamese_search(**parms):
    stop_cluster_elasticserach(parms["ngramSize"])
    execute_cluster_elasticserach(parms["ngramSize"])

    project = 'stackoverflow_filtered'
    properties_path = generate_config_file(parms)
    output_path = f'/home/denis/programming/scripts-siamese/output_{parms["algorithm"]}'
    command = f'java -jar siamese-0.0.6-SNAPSHOT.jar -c search -i ../siamese-optmization/Siamese/my_index/{project} -o ./output_{parms["algorithm"]} -cf ./{properties_path}'
    process = subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    process.wait()

    stop_cluster_elasticserach(parms["ngramSize"])
    most_recent_siamese_output = most_recent_file(output_path)
    new_output_name = properties_path.split('/')[-1].replace('properties', 'csv')
    os.rename(f'{output_path}/{most_recent_siamese_output}', f'{output_path}/{new_output_name}')
    gc.collect()
    os.system('sync')
