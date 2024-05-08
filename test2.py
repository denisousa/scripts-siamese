import pandas as pd

df = pd.read_excel('nsga2_result.xlsx')

filtered_df = df[(df['MRR'] == 0.8681667064819237) & (df['MOP'] == 0.7366231326074231)]

filtered_df.to_excel('EQUAL_BAYESIAN.xlsx', index=False)

print("Filtered data exported to EQUAL_BAYESIAN.csv")
