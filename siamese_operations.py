import pandas as pd
from pprint import pprint
import random
import os
from dotenv import load_dotenv

load_dotenv()


def remove_absolute_path(path):
    return path.split('/')[-1].split('.java')[0] + '.java'

def remove_absolute_path_search_project(path):
    project_to_index = os.getenv('PROJECT_TO_INDEX') + '/'
    return path.split(project_to_index)[-1].split('.java')[0] + '.java'
    #return path.split('/')[-1].split('.java')[0] + '.java'

def get_numbers_from_absolute_path(path):
    return int(path.split("#")[-2]), int(path.split("#")[-1])

def get_method_name(path):
    return path.split('.java_')[-1].split('#')[0]

def format_clones(search_clone, clone):    
    clean_path1 = remove_absolute_path(search_clone)
    start1, end1 = get_numbers_from_absolute_path(search_clone)
    method1 = get_method_name(search_clone)
        
    clean_path2 = remove_absolute_path_search_project(clone)
    start2, end2 = get_numbers_from_absolute_path(clone)
    method2 = get_method_name(clone)

    return {
        "file1": clean_path1,
        "start1": start1,
        "end1": end1,
        "method1": method1,
        "file2": clean_path2,
        "start2": start2,
        "end2": end2,
        "method2": method2
    }


def get_path_from_project_to_index(path):
    projects_path = os.getenv('PROJECT_TO_INDEX')

    if './' in projects_path:
        projects_path = projects_path.replace('./', '')

    path = path.split('/qualitas_corpus_clean/')[-1]
    
    return path


def format_siamese_output(output_path, siamese_output_name):
    siamese_clones = []
    csv_lines = [line for line in open(f'{output_path}/{siamese_output_name}', 'r').read().rstrip().split('\n')]

    for line in csv_lines:
        search_clone, indexed_clones = line.split(',')[0], line.split(',')[1:]
        [siamese_clones.append(format_clones(search_clone, clone)) for clone in indexed_clones]

    df_siamese_clones = pd.DataFrame(data=siamese_clones)
    #df_siamese_clones["file1"] = df_siamese_clones["file1"].apply(get_path_from_project_to_search)
    #df_siamese_clones["file2"] = df_siamese_clones["file2"].apply(get_path_from_project_to_index)
    return df_siamese_clones

