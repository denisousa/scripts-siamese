from elasticsearch_operations import execute_cluster_elasticserach
from time import sleep

for ngram_i, port in zip(range(4,25), range(9200,9221)):
    execute_cluster_elasticserach(ngram_i)
sleep(30)