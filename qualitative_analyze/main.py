import pandas as pd
from siamese_operations import format_siamese_output
from collections import Counter 
from configurations import so_path, qa_path, siamese_csv_results, siamese_csv_results_folder
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

for csv_result in siamese_csv_results:
    result_filename = csv_result.replace('.csv', '')
    open(f'./siamese_code_results/{result_filename}.txt', 'w').write('')
    df_siamese = format_siamese_output(siamese_csv_results_folder, csv_result)
    open(f'./siamese_code_results/{result_filename}.txt', 'a').write(f'SIAMESE OUTPUT CODE ANALYZE \n')
    open(f'./siamese_code_results/{result_filename}.txt', 'a').write(f'{csv_result} \n\n\n')
    df_siamese['start1'] = df_siamese['start1'].astype(int)
    df_siamese['start2'] = df_siamese['start2'].astype(int)
    df_siamese['end1'] = df_siamese['end1'].astype(int)
    df_siamese['end2'] = df_siamese['end2'].astype(int)

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

        qa_code_cut = qa_code.split('\n')[row['start2']-1:row['end2']]
        qa_code_cut = '\n'.join(qa_code_cut)
        status = '\n' + 'StackOverflow File: ' + str((row['file1'], row['start1'], row['end1'], row['method1'])) + '\n' + 'Qualitas File: ' + str((row['file2'].split('/')[-1], row['start2'], row['end2'], row['method2'])) + '\n'
        open(f'./siamese_code_results/{result_filename}.txt', 'a').write(status)
        open(f'./siamese_code_results/{result_filename}.txt', 'a').write(f'\nQualitas Corpus - {row["file2"]} \n' + qa_code_cut + '\n')
        open(f'./siamese_code_results/{result_filename}.txt', 'a').write(f'\nStackOverflow - {row["file1"]} \n' + so_code_cut + '\n\n\n')
        open(f'./siamese_code_results/{result_filename}.txt', 'a').write('===========================================================================================\n')
