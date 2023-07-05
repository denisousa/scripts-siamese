'''
This Script only works in CMD/Terminal
'''


import pandas as pd
from siamese_operations import format_siamese_output
from collections import Counter 
import os
import re

def count_repeated_items(lst):
    counter = Counter(lst)
    repeated_items = [item for item, count in counter.items() if count > 1]
    unique_items = [item for item, count in counter.items() if count == 1]
    return repeated_items, unique_items

def remove_comments(java_code):
    java_code = re.sub(r'\n\s*\n', '\n', java_code) # Blank line
    java_code = re.sub(r'//.*', '', java_code) # // comment
    java_code = re.sub(r'/\*(.*?)\*/', '', java_code, flags=re.DOTALL) # /**/ comment
    
    return java_code
'''
open('clones_analyse_oracle.txt', 'w').write('')
qa_path = 'Siamese-main/my_index/qualitas_corpus_clean'
so_path = 'Siamese-main/my_index/stackoverflow_filtered'
df_oracle = pd.read_csv('clones.csv')
df_oracle['start1'] = df_oracle['start1'].astype(int)
df_oracle['start2'] = df_oracle['start2'].astype(int)
df_oracle['end1'] = df_oracle['end1'].astype(int)
df_oracle['end2'] = df_oracle['end2'].astype(int)
df_oracle.drop('notes', axis=1, inplace=True)
df_oracle.drop('classification', axis=1, inplace=True)

for index, row in df_oracle.iterrows():
    so_file = f'{so_path}/' + row['file1'] 
    so_code = open(so_file, 'r').read()
    so_code_cut = so_code.split('\n')[row['start1']-1:row['end1']]
    so_code_cut = '\n'.join(so_code_cut)

    qa_file = f'{qa_path}/' + row['file2']
    try:
        qa_code = open(qa_file, 'r').read()
    except:
        print(f'problem: {qa_file}', index, '\n')
        continue
    
    qa_code = remove_comments(qa_code)
    qa_code_cut = qa_code.split('\n')[row['start2']-1:row['end2']]
    qa_code_cut = '\n'.join(qa_code_cut)
    status = '\n' + 'StackOverflow File: ' + row['file1'] + '\n' + 'Qualitas File: ' + row['file2'] + '\n'
    open('clones_analyse_oracle.txt', 'a').write(str(row) + status + '\n')
    open('clones_analyse_oracle.txt', 'a').write('\nQA CODE \n' + qa_code_cut + '\n')
    open('clones_analyse_oracle.txt', 'a').write('\nSO CODE \n' + so_code_cut + '\n\n\n')
    open('clones_analyse_oracle.txt', 'a').write('===========================================================================================\n')
'''

open('clones_analyse_siamese.txt', 'w').write('')
df_siamese = format_siamese_output('.', 'qualitas_corpus_n_gram_4_qr_04-07-23_16-31-27.csv')
df_siamese['start1'] = df_siamese['start1'].astype(int)
df_siamese['start2'] = df_siamese['start2'].astype(int)
df_siamese['end1'] = df_siamese['end1'].astype(int)
df_siamese['end2'] = df_siamese['end2'].astype(int)

lst = list(df_siamese['file1'])
repeated_items, unique_items = count_repeated_items(lst)
open('clones_analyse_siamese.txt', 'a').write(f"Quantidade de itens repetidos: {len(repeated_items)} \n")
open('clones_analyse_siamese.txt', 'a').write(f"Quantidade de itens não repetidos: {len(unique_items)} \n")

so_path = 'Siamese-main/my_index/stackoverflow_filtered'
qa_path = 'Siamese-main/my_index/qualitas_corpus_clean'
for index, row in df_siamese.iterrows():
    so_file = f'{so_path}/' + row['file1']
    so_code = open(so_file, 'r').read()
    so_code_cut = so_code.split('\n')[row['start1']-1:row['end1']]
    so_code_cut = '\n'.join(so_code_cut)

    qa_file = f'{qa_path}/' + row['file2']
    try:
        qa_code = open(qa_file, 'r').read()
    except:
        print(f'problem: {qa_file}', index, '\n')
        continue
    
    # qa_code = remove_comments(qa_file)
    qa_code_cut = qa_code.split('\n')[row['start2']-1:row['end2']]
    qa_code_cut = '\n'.join(qa_code_cut)
    status = '\n' + 'StackOverflow File: ' + row['file1'] + '\n' + 'Qualitas File: ' + row['file2'] + '\n'
    open('clones_analyse_siamese.txt', 'a').write(str(row) + status + '\n')
    open('clones_analyse_siamese.txt', 'a').write('\nQA CODE \n' + qa_code_cut + '\n')
    open('clones_analyse_siamese.txt', 'a').write('\nSO CODE \n' + so_code_cut + '\n\n\n')
    open('clones_analyse_siamese.txt', 'a').write('===========================================================================================\n')
