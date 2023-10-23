from elasticsearch_operations import execute_cluster_elasticserach, stop_cluster_elasticserach
from files_operations import most_recent_file
import subprocess
import uuid
import os
import gc
import re

def finish_siamese_process(output_path, properties_path):
    most_recent_siamese_output, _ = most_recent_file(output_path)
    new_output_name = properties_path.split('/')[-1].replace('.properties', f'_{uuid.uuid4()}.csv')
    os.rename(f'{output_path}/{most_recent_siamese_output}', f'{output_path}/{new_output_name}')
    gc.collect()
    os.system('sync')

def get_config_path(parms):
    clonesSize = f'cS_{parms["minCloneSize"]}_'
    ngramSize = f'nS_{parms["ngramSize"]}_'
    QRPercentileNorm = f'qrN_{parms["QRPercentileNorm"]}_'
    QRPercentileT2 = f'qrT2_{parms["QRPercentileT2"]}_'
    QRPercentileT1 = f'qrT1_{parms["QRPercentileT1"]}_'
    QRPercentileOrig = f'qrO_{parms["QRPercentileOrig"]}_'
    normBoost = f'boN_{parms["normBoost"]}_'
    t2Boost = f'boT2_{parms["t2Boost"]}_'
    t1Boost = f'boT1_{parms["t1Boost"]}_'
    origBoost = f'boOr_{parms["origBoost"]}_'
    simThreshold = f'simT_{parms["simThreshold"]}'
    config_name = ngramSize + clonesSize + QRPercentileNorm + QRPercentileT2 + QRPercentileT1 + QRPercentileOrig  + normBoost + t2Boost + t1Boost + origBoost + simThreshold
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
    config = config.replace('QRPercentileNorm=10', f'QRPercentileNorm={parms["QRPercentileNorm"]}')
    config = config.replace('QRPercentileT2=10', f'QRPercentileT2={parms["QRPercentileT2"]}')
    config = config.replace('QRPercentileT1=10', f'QRPercentileT1={parms["QRPercentileT1"]}')
    config = config.replace('QRPercentileOrig=10', f'QRPercentileOrig={parms["QRPercentileOrig"]}')
    config = config.replace('normBoost=4', f'normBoost={parms["normBoost"]}')
    config = config.replace('t2Boost=4', f't2Boost={parms["t2Boost"]}')
    config = config.replace('t1Boost=4', f't1Boost={parms["t1Boost"]}')
    config = config.replace('origBoost=1', f'origBoost={parms["origBoost"]}')
    config = config.replace('simThreshold=', f'simThreshold={parms["simThreshold"]}')
    config = config.replace('qualitas_corpus_clean', f'qualitas_corpus_n_gram_{parms["ngramSize"]}')
    
    properties_path = get_config_path(parms)
    open(properties_path, 'w').write(config)
    return properties_path

def execute_siamese_search(**parms):

    stop_cluster_elasticserach(parms["ngramSize"])
    execute_cluster_elasticserach(parms["ngramSize"])

    project = 'cut_stackoverflow_filtered'
    properties_path = generate_config_file(parms)
    output_path = f'./output_{parms["algorithm"]}'
    index_path = f'../siamese-optmization/Siamese/my_index/{project}'

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    command = f'java -jar ./siamese-0.0.6-SNAPSHOT.jar -c search -i {index_path} -o {output_path} -cf ./{properties_path}'
    process = subprocess.Popen(command,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=None,
                               close_fds=True)
    process.wait()

    stdout = process.stdout.read().decode('utf-8')
    print(f'\n\n{stdout}\n\n')


    if 'does not exist' in stdout:
        # In this case the output file is not created
        execute_siamese_search(**parms)

    siamese_result_filename, siamese_result_text = most_recent_file(output_path)
    format_result_text = re.sub(r'\s', '', siamese_result_text)
    if format_result_text == '':
        os.remove(f'{output_path}/{siamese_result_filename}')
        execute_siamese_search(**parms)

    stop_cluster_elasticserach(parms["ngramSize"])
    finish_siamese_process(output_path, properties_path)
