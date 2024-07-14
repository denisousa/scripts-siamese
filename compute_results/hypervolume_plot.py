import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pygmo as pg
import os

plt.ioff()

def compute_reference_point(all_pareto_front, offset):
    all_mrr = [pareto_front[0] for pareto_front in all_pareto_front]
    all_mop = [pareto_front[1] for pareto_front in all_pareto_front]

    return [max(all_mrr) + offset, max(all_mop) + offset]

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
            pareto_front.append([mrr[i], mop[i]])
            current_max_mop = mop[i]
    
    return np.array(pareto_front)

all_excel_file_path = [
    'grid_search_result.xlsx',
    'random_search_result.xlsx',
    'bayesian_search_result_05_05.xlsx',
    'bayesian_search_result_07_03.xlsx',
    'bayesian_search_result_03_07.xlsx',
    'nsga2_result.xlsx'
]

all_points = []
for excel_file_path in all_excel_file_path:
    pareto_front = calculate_pareto_front(excel_file_path, "MRR", "MOP")
    for point in pareto_front:
        all_points.append(point)


plt.figure(figsize=(8, 6))
plt.xlabel('MRR')
plt.ylabel('MOP')
plt.title('Pareto Front and Hypervolume')

# ref_point = np.array([1.0, 1.0])
ref_point = compute_reference_point(all_points, 0.01)
plt.plot(ref_point[0], ref_point[1], marker='o', markersize=8, label=f'reference point')
for excel_file_path in all_excel_file_path:
    
    label_name = excel_file_path.split('.')[0]
    pareto_front = calculate_pareto_front(excel_file_path, "MRR", "MOP")

    plt.plot(pareto_front[:, 0], pareto_front[:, 1], marker='o', linestyle='-', label=label_name)
    plt.legend()

    plt.fill_between(pareto_front[:, 0], pareto_front[:, 1], ref_point[1], color='gray', alpha=0.3)

    plt.grid(True)
    plt.savefig("hypervolume")
    
plt.close('all')
