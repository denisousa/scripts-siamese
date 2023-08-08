from grid_search import execute_grid_search
from random_search import execute_random_search
from bayesian_optimization import execute_bayesian_search
from kill_all_elasticsearch import kill_all_clusters

kill_all_clusters()
execute_grid_search()
kill_all_clusters()
execute_random_search()
kill_all_clusters()
execute_bayesian_search()