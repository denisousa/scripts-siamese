from grid_search import execute_grid_search
from random_search import execute_random_search
from bayesian_search import execute_bayesian_search
from download_datasource import download_projects
from siamese_indexing import execute_indexing
import argparse


download_projects()
execute_indexing()
execute_grid_search()