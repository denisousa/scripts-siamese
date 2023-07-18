import subprocess
import os
import pandas as pd
from elasticsearch_operations import execute_cluster_elasticserach, stop_cluster_elasticserach
import os
import gc

def check_siamese_execution(process):
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        print('Process executed successfully')
    else:
        print('Error during process execution')

def most_recent_file(directory):
    files = os.listdir(directory)
    paths = [os.path.join(directory, file) for file in files]
    most_recent = max(paths, key=os.path.getctime)
    most_recent_name = os.path.basename(most_recent)
    return most_recent_name

def get_config_path(parms):
    clonesSize = f'cloneSize-{parms["minCloneSize"]}_'
    ngramSize = f'ngramSize-{parms["ngramSize"]}_'
    qrNorm = f'qrNorm-{parms["QRPercentileNorm"]}_'
    qrT2 = f'qrT2-{parms["QRPercentileT2"]}_'
    qrT1 = f'qrT1-{parms["QRPercentileT1"]}_'
    qrOrig = f'qrOrig-{parms["QRPercentileOrig"]}_'
    normBoost = f'normBoost-{parms["normBoost"]}_'
    t2Boost = f't2Boost-{parms["t2Boost"]}_'
    t1Boost = f't1Boost-{parms["t1Boost"]}_'
    origBoost = f'origBoost-{parms["origBoost"]}'
    config_name = clonesSize + ngramSize + qrNorm + qrT2 + qrT1 + qrOrig + t2Boost + t1Boost + normBoost + origBoost
    destination_file = f'./{parms["config_folder"]}'
    return f'{destination_file}/{config_name}.properties'

def generate_config_file(parms):
    elasticsearch_path = '/home/denis/programming/siamese-optmization/elasticsearch-siamese'
    elasticsearch_path = f'{elasticsearch_path}/elasticsearch-ngram-{parms["ngramSize"]}'


    config = open('search-config.properties', 'r').read()
    config = config.replace('elasticsearchLoc=elasticsearchLoc', f'elasticsearchLoc={elasticsearch_path}')
    config = config.replace('outputFolder=search_results', f'outputFolder={parms["output_folder"]}')
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
    config = config.replace('qualitas_corpus_clean', f'qualitas_corpus_n_gram_{parms["ngramSize"]}')
    
    properties_path = get_config_path(parms)
    open(properties_path, 'w').write(config)
    return properties_path

def execute_siamese_search(**parms):
    try:
        stop_cluster_elasticserach(parms["ngramSize"])
        execute_cluster_elasticserach(parms["ngramSize"])

        project = 'stackoverflow_filtered'
        output_path = '/home/denis/programming/scripts-siamese/output_grid_search'
        properties_path = generate_config_file(parms)
        command = f'java -jar siamese-0.0.6-SNAPSHOT.jar -c search -i ../siamese-optmization/Siamese/my_index/{project} -o ./{parms["output_folder"]} -cf ./{properties_path}'
        process = subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        process.wait()
        check_siamese_execution(process)

        stop_cluster_elasticserach(parms["ngramSize"])
        most_recent_siamese_output = most_recent_file(output_path)
        new_output_name = properties_path.split('/')[-1].replace('properties', 'csv')
        os.rename(f'{output_path}/{most_recent_siamese_output}', f'{output_path}/{new_output_name}')
        #df_siamese = format_siamese_output(output_path, most_recent_siamese_output)
        #df_clones = pd.read_csv('clones.csv')
        #df_clones = filter_oracle(df_clones)
        gc.collect()
        os.system('sync')
    except:
        open('errors_gridsearch.txt', 'a').write(str(parms.values()))
        open('errors_gridsearch.txt', 'a').write('\n\n')