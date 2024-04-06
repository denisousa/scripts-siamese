import pandas as pd
import json
import matplotlib.pyplot as plt
import statistics


def round_values(x):
    return round(x, 4)

def get_metrics(paths):
    metrics = {}
    overview = {}
    for file_path in paths:
        file_path_formatted = file_path.replace(".xlsx", "")
        df = pd.read_excel(file_path)
        metrics[file_path_formatted] = df[metric].astype(float).tolist()
        overview[file_path_formatted] = {}
        overview[file_path_formatted]['max'] = max(metrics[file_path_formatted])
        overview[file_path_formatted]['min'] = min(metrics[file_path_formatted])
        overview[file_path_formatted]['median'] = statistics.median(metrics[file_path_formatted])
    
    return metrics, overview

algorithms_labels = ['Grid Search',
          'Random Search',
          'Bayesian Search (05,05)',
          'Bayesian Search (07,03)',
          'Bayesian Search (03,07)']

metrics = ['MRR', 'MOP'] # MRR, MOP, WA(MRR,MOP)
metric_labels = ['Mean Reciprocal Rank (MRR)', 'Mean Overall Precision (MOP)']

overview = {}

for i, metric in enumerate(metrics):

    results_optimization = [
        'grid_search_result.xlsx',
        'random_search_result.xlsx',
        'bayesian_search_result_05_05.xlsx',
        'bayesian_search_result_07_03.xlsx',
        'bayesian_search_result_03_07.xlsx',
        # 'nsga2_result.xlsx'
    ]
    results_dict, overview_metrics = get_metrics(results_optimization)
    overview[metric] = overview_metrics
    colors = ['lightblue', 'lightgreen', '#8A2BE2']
    fig, axs = plt.subplots(figsize=(14, 8))
    axs.boxplot(results_dict.values())
    axs.set_xticklabels(['','','','',''], fontsize=20)
    #plt.xticks(rotation=45)

    #plt.suptitle(f'Siamese - {metric} Results')
    axs.tick_params(axis='both', labelsize=16)
    plt.ylabel(metric_labels[i], rotation=90, labelpad=20, fontsize=20, fontweight='bold')
    #plt.show()
    plt.savefig(f"results_boxplot/boxplot_{metric}")
    plt.close('all')

output_file_path = "boxplot.json"

with open(output_file_path, "w") as json_file:
    json.dump(overview, json_file, indent=4)

'''import statistics
from tabulate import tabulate
import matplotlib.pyplot as plt
from io import BytesIO

def generate_table(grid_search_metric, random_search_metric, bayesian_search_metric):
    grid_search_stats = [max(grid_search_metric), min(grid_search_metric), statistics.median(grid_search_metric)]
    random_search_stats = [max(random_search_metric), min(random_search_metric), statistics.median(random_search_metric)]
    bayesian_search_stats = [max(bayesian_search_metric), min(bayesian_search_metric), statistics.median(bayesian_search_metric)]

    table = [
        ["", "Max", "Min", "Median"],
        ["Grid Search", *grid_search_stats],
        ["Random Search", *random_search_stats],
        ["Bayesian Optimization", *bayesian_search_stats]
    ]

    print(tabulate(table, headers="firstrow", tablefmt="grid"))

    fig, ax = plt.subplots()
    ax.axis("off")
    ax.table(cellText=table, colLabels=None, cellLoc="center", loc="center")
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    
    plt.show()

generate_table(grid_search_metric, random_search_metric, bayesian_search_metric)'''
