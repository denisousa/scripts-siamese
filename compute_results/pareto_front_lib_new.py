from paretoset import paretoset
import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_image(mrr, mop, pareto_front, path):
    plt.scatter(mrr, mop, label='Data')
    plt.plot(*zip(*pareto_front), color='red', label='Pareto Front')
    plt.title('Pareto Front')
    plt.xlabel('MRR')
    plt.ylabel('MOP')
    plt.legend()
    plt.grid(True)
    plt.savefig(path)
    plt.close('all')

excel_file_path_list = [
    'old_grid_search_result.xlsx',
    'random_search_result.xlsx',
    'bayesian_search_result_05_05.xlsx',
    'bayesian_search_result_07_03.xlsx',
    'bayesian_search_result_03_07.xlsx',
    # 'nsga2_result.xlsx'
]

labels = [
'Grid Search',
'Random Search',
'Bayesian Search (0.5, 0.5)',
'Bayesian Search (0.7, 0.3)',
'Bayesian Search (0.3, 0.7)',
]


fig, ax = plt.subplots(figsize=(10, 6))
for i, excel_file_path in enumerate(excel_file_path_list):
    excel_data = pd.read_excel(excel_file_path)

    mrr_column = 'MRR'  
    mop_column = 'MOP' 

    mrr = excel_data[mrr_column].tolist()
    mop = excel_data[mop_column].tolist()

    metrics = pd.DataFrame({"mrr": mrr,
                            "mop": mop})

    mask = paretoset(metrics, sense=["max", "max"])
    pareto_front_df = metrics[mask]
    #pareto_front_df.to_csv(labels[i] + ".csv", index=False)
    
    pareto_front = sorted([(x['mrr'], x['mop']) for _, x in pareto_front_df.iterrows()])
    

    ax.plot(*zip(*pareto_front), label=labels[i])
    ax.set_xlabel('MRR')
    ax.set_ylabel('MOP')
    ax.legend()
    ax.grid(True)

plt.show()
plt.savefig('pareto_front')
plt.close('all')