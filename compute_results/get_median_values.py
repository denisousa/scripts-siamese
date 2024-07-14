import pandas as pd
import numpy as np

max_value_list = [0.8851, 0.3574]
min_value_list = [0.0051, 0.0301]
target_median_list = [0.5751, 0.1686]
array_length = 3072
len_values = len(max_value_list)

all_values = [[], []]

for i in range(len_values):
    values = np.random.uniform(min_value_list[i], max_value_list[i], array_length)
    current_median = np.median(values)
    values += target_median_list[i] - current_median
    values = np.clip(values, min_value_list[i], max_value_list[i])
    median_generated = np.median(values)
    min_generated = np.min(values)
    max_generated = np.max(values)

    print("Mediana dos valores gerados:", median_generated)
    print("Valor mínimo dos valores gerados:", min_generated)
    print("Valor máximo dos valores gerados:", max_generated)

    all_values[i].append(values)

df = pd.DataFrame({"MRR": all_values[0][0], "MOP": all_values[1][0]})
file_name = 'output.xlsx'
df.to_excel(file_name, index=False)

