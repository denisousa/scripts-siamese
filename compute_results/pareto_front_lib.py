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

excel_file_path_list = os.listdir("results_optimization")

for excel_file_path in excel_file_path_list:
    excel_data = pd.read_excel(excel_file_path)

    mrr_column = 'MRR'  
    mop_column = 'MOP' 

    mrr = excel_data[mrr_column].tolist()
    mop = excel_data[mop_column].tolist()

    metrics = pd.DataFrame({"mrr": mrr,
                            "mop": mop})

    mask = paretoset(metrics, sense=["max", "max"])
    pareto_set_metrics = metrics[mask]

    excel_file_path_formatted = excel_file_path.replace(".xlsx", "") 
    path = f"results_optimization_figure_lib/{excel_file_path_formatted}"

    pareto_set_metrics = pareto_set_metrics.sort_values(by='mrr', ascending=False)
    pareto_set_metrics.reset_index(drop=True, inplace=True)
    pareto_set_metrics.to_csv(path + ".csv", index=False)

    generate_image(mrr, mop, pareto_set_metrics, path)