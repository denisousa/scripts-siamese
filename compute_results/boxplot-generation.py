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

algorithms_labels = [
    'Grid Search',
    'Random Search',
    'Bayesian Search (05,05)',
    'Bayesian Search (07,03)',
    'Bayesian Search (03,07)',
    'NSGA-II'
]

metrics = ['MRR', 'MOP'] # MRR, MOP, WA(MRR,MOP)
metric_labels = ['MRR', 'MOP']

overview = {}

for i, metric in enumerate(metrics):

    results_optimization = [
        'grid_search_result.xlsx',
        'random_search_result.xlsx',
        'bayesian_search_result_05_05.xlsx',
        'bayesian_search_result_07_03.xlsx',
        'bayesian_search_result_03_07.xlsx',
        'nsga2_result.xlsx'
    ]
    results_dict, overview_metrics = get_metrics(results_optimization)
    overview[metric] = overview_metrics
    colors = ['lightblue', 'lightgreen', '#8A2BE2']
    fig, axs = plt.subplots(figsize=(14, 8))
    axs.boxplot(results_dict.values())
    axs.set_xticklabels(['','','','','',''], fontsize=20)
    #axs.set_xticklabels(algorithms_labels, fontsize=20)
    #plt.xticks(rotation=45)

    #plt.suptitle(f'Siamese - {metric} Results')
    axs.tick_params(axis='both', labelsize=16)
    plt.ylabel(metric_labels[i], rotation=90, labelpad=20, fontsize=20, fontweight='bold')
    #plt.show()
    plt.savefig(f"boxplot_{metric}")
    plt.close('all')

output_file_path = "boxplot.json"

with open(output_file_path, "w") as json_file:
    json.dump(overview, json_file, indent=4)
