import datetime
from grid_search import execute_grid_search
from download_datasource import download_projects
from siamese_indexing import execute_indexing
from generate_metrics import get_metrics

ini = datetime.datetime.now()

download_projects()
execute_indexing()

grid_temp = execute_grid_search()

optimization_algorithms = ['grid_search']
temp = [grid_temp]
get_metrics(optimization_algorithms, temp)


time_difference = datetime.datetime.now() - ini

print(time_difference)
open("experiment_grid_time.txt","w").write(f"{time_difference}")
