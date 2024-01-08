import requests
from elasticsearch_operations import create_one_cluster_elasticserach, execute_cluster_elasticserach, stop_cluster_elasticserach
from elasticsearch import Elasticsearch

ngram = 4
port = 9000 + ngram
create_one_cluster_elasticserach(ngram)
stop_cluster_elasticserach(ngram)
execute_cluster_elasticserach(ngram)
elasticsearch_url = f"http://localhost:{port}"
index_name = f"qualitas_corpus_n_gram_{ngram}"
node_name = 'master'


es = Elasticsearch(elasticsearch_url)

index_settings = {
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 1
    }
}

es.indices.create(index=index_name, body=index_settings)

'''
curl -XGET 'localhost:9004/_cat/indices?v'
curl -XGET 'localhost:9004/qualitas_corpus_n_gram_4/_settings'

curl -XPOST 'http://localhost:9004/_cluster/reroute?retry_failed=true'
curl -XGET 'http://localhost:9004/_cat/shards'
curl -XGET 'http://localhost:9004/_cat/shards?v'
curl -XGET 'http://localhost:9004/_cluster/health'
curl -XGET 'http://localhost:9004/_cat/nodes?v'
curl -XDELETE http://localhost:9004/nome_do_indice
'''