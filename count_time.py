from datetime import datetime, timedelta
import pandas as pd

def find_lines_with_runtime(filename):
    result = []
    with open(filename, 'r') as file:
        for line in file:
            if 'Runtime:' in line:
                result.append(line.strip().replace('Runtime: ', ''))
    return result


file_path = "mrr_result.xlsx"  # Substitua pelo caminho correto do seu arquivo
df = pd.read_excel(file_path)

# Extraia os valores da coluna "time" em uma lista
time_values = df["time"].tolist()

time_format = "%H:%M:%S.%f"
runtimes = [datetime.strptime(runtime, time_format) for runtime in time_values]
runtimes = [timedelta(minutes=r.minute, seconds=r.second) for r in runtimes]

count = timedelta(seconds=0)
for r in runtimes:
    try:
        count += r
    except:
        print(r)

print(count)
