import requests
from elasticsearch_operations import create_one_cluster_elasticserach, execute_cluster_elasticserach, stop_cluster_elasticserach

ngram = 4
port = 9000 + ngram
create_one_cluster_elasticserach(ngram)
stop_cluster_elasticserach(ngram)
execute_cluster_elasticserach(ngram)
elasticsearch_url = f"http://localhost:{port}"
index_name = f"qualitas_corpus_n_gram_{ngram}"

'''endpoint = f"{elasticsearch_url}/_cluster/settings?pretty"
payload = {
    "transient" : {
        "cluster.routing.allocation.enable" : "all"
    }
}

response = requests.put(endpoint, json=payload)'''

node_name = 'master'
endpoint = f"{elasticsearch_url}/{index_name}"
payload = {
    "settings": {
        "number_of_shards": 3,
        #"number_of_replicas": 1,
        #"routing.allocation.include._name": node_name
    }
}

response = requests.put(endpoint, json=payload)

if response.status_code == 200:
    print(f"Successfully updated the number of replicas for index '{index_name}' with {payload}.")
else:
    print(f"Failed to update the number of replicas. Status code: {response.status_code}, Response: {response.text}")

endpoint = f"{elasticsearch_url}/{index_name}/_settings"
payload = {
    "index": {
        #"number_of_shards": 3,
        "number_of_replicas": 1,
        #"routing.allocation.include._name": node_name
    }
}

response = requests.put(endpoint, json=payload)

'''payload = {
  "commands": [
    {
      "allocate_stale_primary": {
        "index": index_name,
        "shard": 0,
        "node": node_name
      }
    },
    {
      "allocate_stale_primary": {
        "index": index_name,
        "shard": 1,
        "node": node_name
      }
    }
  ]
}

endpoint = f"{elasticsearch_url}/_cluster/reroute"
response = requests.post(endpoint, json=payload)

if response.status_code == 200:
    print(f"Successfully. Status code: {response.status_code}, Response: {response.text}")
else:
    print(f"Failed. Status code: {response.status_code}, Response: {response.text}")'''


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