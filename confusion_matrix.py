import pandas as pd
from pprint import pprint
from siamese_operations import format_siamese_output
import json

def get_metric(tp, fp, fn):
    recall = tp/(tp+fn)
    precision = tp/(tp+fp)
    f1_score = 2*((precision*recall)/(precision+recall))
    
    if precision == 0 or recall == 0:
        return 0, 0, 0
    
    return recall, precision, f1_score

def get_confusion_matrix(df_siamese, df_clones):
    merged_df = pd.merge(df_siamese, df_clones, on=['file1', 'file2'], how='inner')
    
    start1_condition = merged_df['start1_x'] >= merged_df['start1_y']
    end1_condition = merged_df['end1_x'] <= merged_df['end1_y']
    
    start2_condition = merged_df['start2_x'] >= merged_df['start2_y']
    end2_condition = merged_df['end2_x'] <= merged_df['end2_y']
    
    filter_df1 = merged_df[start1_condition & end1_condition & start2_condition & end2_condition]

    start1_condition = merged_df['start1_x'] <= merged_df['start1_y']
    end1_condition = merged_df['end1_x'] >= merged_df['end1_y']
    
    start2_condition = merged_df['start2_x'] <= merged_df['start2_y']
    end2_condition = merged_df['end2_x'] >= merged_df['end2_y']

    filter_df2 = merged_df[start1_condition & end1_condition & start2_condition & end2_condition]
    filter_df = pd.merge(filter_df1, filter_df2, how='outer')

    tp = filter_df.shape[0]

    fn = df_clones.shape[0] - filter_df.shape[0]

    fp = df_siamese.shape[0] - (tp + fn)
    return tp, fp, fn

def replace_so(string_value):
    return string_value.replace('stackoverflow_filtered/', '')

def replace_qa(string_value):
    return string_value.replace('qualitas_corpus_filtered/', '')

def check_exists_equal_row(df, row):
    '''
    TP - É clone e o Siamese detectou clone -> OK
    FP - Não é clone, mas o Siamese detectou clone -> PROBLEMA
    TN - Não é clone e o Siamese não detectou clone -> NÂO IMPORTA
    FN - É um clone, mas a ferramenta não encontrou -> OK
    '''
    for i, r in df.iterrows():
        file1_condition = r['file1'] == row['file1']
        start1_condition = r['start1'] == row['start1']
        end1_condition = r['end1'] == row['end1']
        
        file2_condition = r['file2'] == row['file2']
        start2_condition = r['start2'] == row['start2']
        end2_condition = r['end2'] == row['end2']
        
        cond1 = file1_condition and start1_condition and end1_condition
        cond2 = file2_condition and start2_condition and end2_condition

        if cond1 and cond2:
            result_tp.append(r)
        
        if file1_condition and file2_condition:
            result_files.append(r)

def generate_confusion_matrix(df_siamese, df_clones):
    df_siamese['file1'] = df_siamese['file1'].apply(replace_so)
    df_siamese['file2'] = df_siamese['file2'].apply(replace_qa)
    # df_siamese.to_csv(index=False)
    df_siamese.drop('method1', axis=1, inplace=True)
    df_siamese.drop('method2', axis=1, inplace=True)

    df_clones.reset_index(drop=True, inplace=True)
    df_siamese.reset_index(drop=True, inplace=True)

    tp, fp, fn = get_confusion_matrix(df_siamese, df_clones)
    recall, precision, f1_score = get_metric(tp, fp, fn)
    return recall, precision, f1_score
