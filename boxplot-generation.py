import pandas as pd
import matplotlib.pyplot as plt
import statistics

def round_values(x):
    return round(x, 4)

metric = 'MRR'

def get_metrics(paths):
    metrics = []
    for file_path in paths:
        df = pd.read_excel(file_path)
        metrics.append(list(map(round_values, df[metric].astype(float).tolist())))
    return metrics

mrr_list = get_metrics(['grid_search_result.xlsx',
             'random_search_result.xlsx',
             'bayesian_search_result.xlsx',])

grid_search_metric = mrr_list[0]
random_search_metric = mrr_list[1]
bayesian_search_metric = mrr_list[2]

colors = ['lightblue', 'lightgreen', '#8A2BE2']

results_dict = {'Grid Search': mrr_list[0], 'Random Search': mrr_list[1], 'Bayesian Search': mrr_list[2]}

fig, axs = plt.subplots()
axs.boxplot(results_dict.values())
axs.set_xticklabels(results_dict.keys())


'''axs[0].boxplot(grid_search_metric, patch_artist=True, boxprops=dict(facecolor=colors[0]))
axs[0].set_title('Grid Search')

axs[1].boxplot(random_search_metric, patch_artist=True, boxprops=dict(facecolor=colors[1]))
axs[1].set_title('Random Search')

axs[2].boxplot(bayesian_search_metric, patch_artist=True, boxprops=dict(facecolor=colors[2]))
axs[2].set_title('Bayesian Search')

for ax in axs:
    ax.set_xticklabels([''])
    ax.set_ylabel('MRR')
    ax.grid(True)'''

plt.suptitle('Siamese - MRR Results')
plt.show()


import statistics
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

generate_table(grid_search_metric, random_search_metric, bayesian_search_metric)
