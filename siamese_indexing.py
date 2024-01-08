"""
Indexing
r1, r2, and r3 starting from 4 to 24 (step of 4) - Siamese Research
r1, r2, and r3 starting from 4 to 24 (step of 1 or 2) - Denis Research

Search
The query reduction thresholds should be somewhere around 1-15%

"""
import os
import gc
import subprocess
from elasticsearch_operations import (
    execute_cluster_elasticserach,
    stop_cluster_elasticserach,
    create_one_cluster_elasticserach
)
from dotenv import load_dotenv

load_dotenv()


def execute_siamese_index_properties(ngram):
    gc.collect()
    os.system("sync")
    create_one_cluster_elasticserach(ngram)
    stop_cluster_elasticserach(ngram)
    execute_cluster_elasticserach(ngram)
    # put_template(ngram)

    project_index_path = os.getenv("PROJECT_TO_INDEX")
    elasticsearch_path = os.getenv("ELASTICSEARCH_CLUSTERS")

    n_gram_properties_path = "./n-gram-properties"

    index_name = os.getenv("INDEX_NAME")
    index_name = f"{index_name}_n_gram_{ngram}"

    config = open("config-index.properties", "r").read()
    config = config.replace(
        "elasticsearchLoc=", f"elasticsearchLoc={elasticsearch_path}"
    )
    config = config.replace("cluster=", f"cluster=stackoverflow")
    config = config.replace("index=", f"index={index_name}")
    config = config.replace("t1NgramSize=", f"t1NgramSize={ngram}")
    config = config.replace("t2NgramSize=", f"t2NgramSize={ngram}")
    config = config.replace("ngramSize=", f"ngramSize={ngram}")
    config = config.replace("inputFolder=", f"inputFolder={project_index_path}")
    print(f"CONFIG NAME: {index_name} \n\n")
    new_config = f"{n_gram_properties_path}/n_gram_{ngram}.properties"
    open(new_config, "w").write(config)
    command = f"java -jar siamese-0.0.6-SNAPSHOT.jar -cf {new_config}"
    process = subprocess.Popen(
        command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True
    )
    process.wait()

    stop_cluster_elasticserach(ngram)

initial_quantity = int(os.getenv("INITIAL_CLUSTER_QUANTITY"))
final_quantity = int(os.getenv("FINAL_CLUSTER_QUANTITY")) + 1
clusters_range = range(initial_quantity, final_quantity)

for i in clusters_range:
    execute_siamese_index_properties(i)
