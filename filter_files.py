import pandas as pd
from os import walk
import os
from glob import glob
import shutil
from pprint import pprint


def copy_directories(source_file, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    directories = source_file.split('/')[:-1]
    directory_complete = '.'
    for directory in directories:
        directory_complete = f'{directory_complete}/{directory}'
        os.makedirs(f'{destination_folder}/{directory_complete}', exist_ok=True)

def copy_file(source_file, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    file_name = os.path.basename(source_file)
    shutil.copy2(source_file, destination_folder)
    
def copy_files_directory_from_oracle(df_clones, column, source_path, destination_path):
    for java_file in df_clones[column]:
        directory_base = '/'.join(java_file.split('/')[:-1])
        copy_directories(java_file, destination_path)
        copy_file(f'{source_path}/{java_file}', f'{destination_path}/{directory_base}')
    
    print(f'Sucess copy from: {source_path} to {destination_path}')

df_clones = pd.read_csv('clones.csv')
df_clones = df_clones[(df_clones['classification'] == 'QS') | (df_clones['classification'] == 'EX') | (df_clones['classification'] == 'UD')]
base_path = '/home/denis/Hyperparameter-Optimization-Siamese/Siamese-main/my_index'
# qa_path = f'{base_path}/qualitas_corpus_clean'
so_path = f'{base_path}/stackoverflow_dump'
new_so_path = f'{base_path}/stackoverflow_filtered'
# new_qa_path = f'{base_path}/qualitas_corpus_filtered'

# shutil.rmtree(new_qa_path)
shutil.rmtree(new_so_path)

copy_files_directory_from_oracle(df_clones, 'file1', so_path, new_so_path)
# copy_files_directory_from_oracle('file2', qa_path, new_qa_path)

print(len(list(set(df_clones['file1']))))
# print(len(list(set(df_clones['file2']))))