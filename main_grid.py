from grid_search import execute_grid_search
from download_datasource import download_projects
from siamese_indexing import execute_indexing
from generate_metrics import get_metrics

#download_projects()

#execute_indexing()

grid_temp = execute_grid_search()

optimization_algorithms = ['grid_search']
temp = [grid_temp]
get_metrics(optimization_algorithms, temp)
