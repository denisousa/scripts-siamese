import pandas as pd
from siamese_operations import format_siamese_output
import time


def get_match_clones_with_oracle(df_siamese, df_clones):
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
    return filter_df

'''def calculate_mrr_CHATGPT(predictions, df_clones):
    mrr = 0
    relevants = list(df_clones['file2'])
    for pred, rel in zip(predictions, relevants):
        if rel in pred:
            rank = pred.index(rel) + 1  # Obter a posição do item relevante na lista
            mrr += 1 / rank
    mrr /= len(predictions)
    return mrr

# Exemplo de uso
predictions = [
    ['Item1', 'Item3', 'Item2'],
    ['Item2', 'Item1', 'Item3'],
    ['Item3', 'Item2', 'Item1']
]'''

df_clones = pd.read_csv('clones.csv')
df_siamese = pd.read_csv('df_siamese_formatted.csv')
df_merge = get_match_clones_with_oracle(df_siamese, df_clones)

def check_clone_is_correct(oracle_row, siamese_row):
    # Oracle inside Siamese
    start1_condition = oracle_row['start1'] >= siamese_row['start1']
    end1_condition = oracle_row['end1'] <= siamese_row['end1']

    if start1_condition and end1_condition:
        return True
        
    # Siamese inside Oracle
    start1_condition = oracle_row['start1'] <= siamese_row['start1']
    end1_condition = oracle_row['end1'] >= siamese_row['end1']

    if start1_condition and end1_condition:
        return True

    return False

def calculate_mrr(df_siamese, df_clones):
    # File1 -> Stackoverflow
    # File2 -> Qualitas Corpus
    
    mrr = 0
    so_snippets = list(df_siamese.drop_duplicates(subset='file1')['file1'])
    len_so_snippets = len(so_snippets)

    for so_snippet in so_snippets:
        oracle_filtered_df = df_clones[df_clones['file1'] == so_snippet]
        oracle_filtered_df.reset_index(drop=True, inplace=True)
        
        if oracle_filtered_df.shape[0] == 0:
            mrr += 1 # Estou assumindo 1 ao MRR quando o Siamese acerta um clone fora do oráculo
            continue
        
        siamese_row = df_siamese.loc[df_siamese['file1'] == so_snippet].iloc[0]
        for index, oracle_row in oracle_filtered_df.iterrows():
            file2_condition = oracle_row['file2'] == siamese_row['file2']
            if not file2_condition and index == len(oracle_row):
                mrr += 1
            
            if not file2_condition:
                continue

            clone_is_correct = check_clone_is_correct(oracle_row, siamese_row)
            if clone_is_correct:
                mrr += 1/(index+1)
                break

            if index == len(oracle_row):
                mrr += 0 # Boto 0 quando ele não acerta nada
    
    
    mrr = mrr/len_so_snippets
    print(f'Len SO Snippets: {len_so_snippets}', f'MRR: {mrr}')
    return mrr

start_time = time.time()

calculate_mrr(df_siamese, df_clones)

end_time = time.time()
execution_time = end_time - start_time
print("Tempo de execução:", execution_time, "segundos")

'''
OBS: Quando ele só encontra 1 clone correpondente e está errado, então ele é 0
O que eu faço em relação aos clones que não foram detectados?
'''

# mrr_score = calculate_mrr(predictions, relevants)
# print("Mean Reciprocal Rank (MMR):", mrr_score)
