import matplotlib.pyplot as plt
import statistics
import numpy as np
import pandas as pd
import pygmo as pg
import json


def plot_hypervolume(ref_point, all_excel_path):
    algorithms_labels = [
        'Grid Search',
        'Random Search',
        'Bayesian Search (05,05)',
        'Bayesian Search (07,03)',
        'Bayesian Search (03,07)',
        'NSGA-II'
    ]

    plt.figure(figsize=(6, 8))
    plt.xlabel('MRR')
    plt.ylabel('MOP')
    
    plt.plot(ref_point[0], ref_point[1], marker='o', markersize=8, label=f'Reference Point')

    for i, excel_file_path in enumerate(all_excel_path):
        
        # label_name = excel_file_path.split('.')[0]
        pareto_front = calculate_pareto_front(excel_file_path, "MRR", "MOP")

        plt.plot(pareto_front[:, 0], pareto_front[:, 1], marker='o', linestyle='-', label=algorithms_labels[i])
        plt.legend()

        plt.fill_between(pareto_front[:, 0], pareto_front[:, 1], ref_point[1], color='gray', alpha=0.3)

        plt.grid(True)
        plt.savefig("hypervolume")
        
    plt.show()
    plt.close('all')


def get_all_points(all_excel_path):
    all_points = []
    for excel_file_path in all_excel_path:
        pareto_front = calculate_pareto_front(excel_file_path, "MRR", "MOP")
        for point in pareto_front:
            all_points.append(point)
    return all_points

def compute_ref_point(all_points, offset):
    all_mrr = [pareto_front[0] for pareto_front in all_points]
    all_mop = [pareto_front[1] for pareto_front in all_points]
    return [max(all_mrr) + offset, max(all_mop) + offset]


def compute_hipervolume(pareto_front, ref_point):
    pareto_front = np.array(pareto_front)
    hyp = pg.hypervolume(pareto_front).compute(ref_point)

    return hyp

def calculate_pareto_front(excel_file_path, metric1, metric2):
    excel_data = pd.read_excel(excel_file_path)

    metric1_column = metric1
    metric2_column = metric2

    mrr = excel_data[metric1_column].tolist()
    mop = excel_data[metric2_column].tolist()

    sorted_indices = sorted(range(len(mrr)), key=lambda k: mrr[k])
    mrr = [mrr[i] for i in sorted_indices]
    mop = [mop[i] for i in sorted_indices]

    mrr.reverse()
    mop.reverse()

    pareto_front = []  
    current_max_mop = float('-inf')
    for i in range(len(mop)):
        if mop[i] > current_max_mop:
            pareto_front.append([mrr[i], mop[i]])
            current_max_mop = mop[i]

    return np.array(pareto_front)


all_excel_path = [
'grid_search_result.xlsx',
'random_search_result.xlsx',
'bayesian_search_result_05_05.xlsx',
'bayesian_search_result_07_03.xlsx',
'bayesian_search_result_03_07.xlsx',
'nsga2_result.xlsx'
]

hvs = {}
all_points = get_all_points(all_excel_path)
ref_point = compute_ref_point(all_points, 0.01)

for i, excel_path in enumerate(all_excel_path):
    pareto_front = calculate_pareto_front(excel_path, "MRR", "MOP")
    hv = compute_hipervolume(pareto_front, ref_point)
    
    splitted_label = excel_path.split(".")[0]
    hvs[splitted_label] = hv

output_file_path = "hypervolume.json"

with open(output_file_path, "w") as json_file:
    json.dump(hvs, json_file, indent=4)


plot_hypervolume(ref_point, all_excel_path)