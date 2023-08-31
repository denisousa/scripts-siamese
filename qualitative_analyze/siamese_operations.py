import pandas as pd
from pprint import pprint
import random
import os


def remove_absolute_path(path):
    return path.split('my_index')[-1].split('#')[0].split('.java')[0] + '.java'

def get_numbers_from_absolute_path(path):
    return int(path.split("#")[-2]), int(path.split("#")[-1])

def get_method_name(path):
    return path.split('my_index')[-1].split('#')[0].split('.java')[-1][1:]

def format_clones(search_clone, clone):    
    clean_path1 = remove_absolute_path(search_clone)
    start1, end1 = get_numbers_from_absolute_path(search_clone)
    method1 = get_method_name(search_clone)
        
    clean_path2 = remove_absolute_path(clone)
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

def show_clone_by_index(df, index):
    my_index_path = '/home/denis/Hyperparameter-Optimization-Siamese/Siamese-main/my_index'
    line = df.loc[index]
    path1, path2 = line['file1'], line['file2']
    
    path1, path2 = open(f'{my_index_path}{path1}','r').read(), open(f'{my_index_path}{path2}','r').read()
    path1, path2 = path1.split('\n')[line['start1']-1:line['end1']+1], path2.split('\n')[line['start2']-1:line['end2']+1]
    pprint(path1)
    print('\n\n')
    pprint(path2)
    
def execute_search_siamese(project):
    os.system(f'cd Siamese-main && java -jar siamese-0.0.6-SNAPSHOT.jar -c search -i ./my_index/{project}/ -o ./output -cf config.properties')

def execute_index_siamese(project, config_properties):
    os.system(f'cd Siamese-main && java -jar siamese-0.0.6-SNAPSHOT.jar -c index -i ./my_index/{project}/ -cf {config_properties}')

def get_recall_precision_f1_score(X, Y):
    return random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)

def remove_first_backslash(path):
    if 'cut_stackoverflow_filtered/' in path:
        path = path.replace('cut_stackoverflow_filtered/','')
    
    if 'qualitas_corpus_clean/' in path:
        path = path.replace('qualitas_corpus_clean/','')

    if path[0] == '/':
        return path[1:]
    return path


def format_siamese_output(output_path, siamese_output_name):
    siamese_clones = []
    csv_lines = [line for line in open(f'{output_path}/{siamese_output_name}', 'r').read().rstrip().split('\n')]

    for line in csv_lines:
        search_clone, indexed_clones = line.split(',')[0], line.split(',')[1:]
        [siamese_clones.append(format_clones(search_clone, clone)) for clone in indexed_clones]

    df_siamese_clones = pd.DataFrame(data=siamese_clones)
    df_siamese_clones["file1"] = df_siamese_clones["file1"].apply(remove_first_backslash)
    df_siamese_clones["file2"] = df_siamese_clones["file2"].apply(remove_first_backslash)
    # df_siamese_clones.to_csv(f'formatted_{siamese_output_name}.csv', encoding='utf-8', index=False)
    return df_siamese_clones
    # show_clone_by_index(df_siamese_clones, 0)

