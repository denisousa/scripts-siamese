from grid_search import execute_grid_search
from random_search import execute_random_search
from bayesian_search import execute_bayesian_search
from download_datasource import download_projects
from calculate_metrics import get_metrics

download_projects()
temp = execute_grid_search()
get_metrics("grid_search", temp)