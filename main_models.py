import datetime
from random_search import execute_random_search
from bayesian_search import execute_bayesian_search
from download_datasource import download_projects
from siamese_indexing import execute_indexing
from generate_metrics import get_metrics

ini = datetime.datetime.now()

#download_projects()
#execute_indexing()

random_temp = execute_random_search()
bayesian_temp = execute_bayesian_search()

optimization_algorithms = ['random_search']
temp = [random_temp]
get_metrics(optimization_algorithms, temp)

time_difference = datetime.datetime.now() - ini

print(time_difference)
open("experiment_complete_time.txt","w").write(f"{time_difference}")
