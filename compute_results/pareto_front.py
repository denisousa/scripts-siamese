import matplotlib.pyplot as plt
import pandas as pd
import os

def calculate_pareto_front(excel_file_path, metric1, metric2):
    excel_data = pd.read_excel(excel_file_path)

    mrr_column = metric1
    mop_column = metric2

    mrr = excel_data[mrr_column].tolist()
    mop = excel_data[mop_column].tolist()

    sorted_indices = sorted(range(len(mrr)), key=lambda k: mrr[k])
    mrr = [mrr[i] for i in sorted_indices]
    mop = [mop[i] for i in sorted_indices]

    mrr.reverse()
    mop.reverse()

    pareto_front = [] 
    current_max_mop = float('-inf')
    for i in range(len(mop)):
        if mop[i] > current_max_mop:
            pareto_front.append((mrr[i], mop[i]))
            current_max_mop = mop[i]
    
    return pareto_front

excel_file_path_list = [
    #'GRID_SEARCH.csv',
    #'random_search_result.xlsx',
    'bayesian_search_result_05_05.xlsx',
    #'bayesian_search_result_07_03.xlsx',
    #'bayesian_search_result_03_07.xlsx',
    'nsga2_result.xlsx'
]

labels = [
#'Grid Search',
#'Random Search',
'Bayesian Search (0.5, 0.5)',
#'Bayesian Search (0.7, 0.3)',
#'Bayesian Search (0.3, 0.7)',
'NSGA-II'
]

fig, ax = plt.subplots(figsize=(10, 6))
path = f"results_optimization_figure"

for i, excel_file_path in enumerate(excel_file_path_list):
    if excel_file_path == 'GRID_SEARCH.csv':
        df = pd.read_csv(excel_file_path)
        df.to_csv(f"{path}/{excel_file_path}.csv", index=False)
        pareto_front = list(df.to_records(index=False))
    else:
        pareto_front = calculate_pareto_front(excel_file_path, "MRR", "MOP")
        path_new = excel_file_path.replace(".xlsx", "")
        df = pd.DataFrame(pareto_front, columns=["mrr", "mop"])
        df.to_csv(f"{path}/{path_new}.csv", index=False)
    
    #ax.scatter(mrr, mop, label='Data')
    ax.plot(*zip(*pareto_front), label=labels[i])
    ax.set_xlabel('MRR')
    ax.set_ylabel('MOP')
    ax.legend()
    ax.grid(True)

plt.savefig('pareto_front')
plt.show()
plt.close('all')