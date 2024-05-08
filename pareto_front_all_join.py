import pandas as pd
import matplotlib.pyplot as plt
import os
import json

def find_midpoint_and_endpoints(points):
    sum_x = sum(p[0] for p in points)
    sum_y = sum(p[1] for p in points)
    midpoint = (sum_x / len(points), sum_y / len(points))
    closest_point = min(points, key=lambda p: ((p[0] - midpoint[0])**2 + (p[1] - midpoint[1])**2)**0.5)
    farthest_points = sorted(points, key=lambda p: ((p[0] - midpoint[0])**2 + (p[1] - midpoint[1])**2)**0.5, reverse=True)[:2]
    return midpoint, closest_point, farthest_points


excel_file_path_list = [
'grid_search_result.xlsx',
'random_search_result.xlsx',
'bayesian_search_result_05_05.xlsx',
'bayesian_search_result_07_03.xlsx',
'bayesian_search_result_03_07.xlsx',
'nsga2_result.xlsx'
]

labels = [
    'Grid Search',
    'Random Search',
    'Bayesian-EQ',
    'Bayesian-MRR',
    'Bayesian-MOP',
    'NSGA-II'
]

points_by_algorithm = {}

plt.rcParams.update({'font.size': 12})
for index_excel, caminho_arquivo_excel in enumerate(excel_file_path_list):
    dados_excel = pd.read_excel(caminho_arquivo_excel)

    coluna_mrr = 'MRR' 
    coluna_mop = 'MOP' 

    mrr = dados_excel[coluna_mrr].tolist()
    mop = dados_excel[coluna_mop].tolist()

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

    #plt.scatter(mrr, mop, label='Dados')

    new_path = caminho_arquivo_excel.replace(".xlsx", "")
    name = new_path.replace('_result', '')
    points_by_algorithm[name] = pareto_front 
    plt.plot(*zip(*pareto_front), label=labels[index_excel])
    # plt.title('Pareto Front')
    plt.xlabel('MRR')
    plt.ylabel('MOP')
    plt.legend()
    plt.grid(True)
    plt.savefig("pareto_front")
    plt.savefig('pareto_front.pdf', dpi=300)


#plt.show()

with open('pareto_front.json', "w") as json_file:
    json.dump(points_by_algorithm, json_file, indent=4)

# points = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]

nsga2_points = points_by_algorithm['nsga2']
midpoint, closest_point, farthest_points = find_midpoint_and_endpoints(nsga2_points)
print("NSGA-II")
print("Midpoint:", midpoint)
print("Closest point to the midpoint:", closest_point)
print("Points farthest from the midpoint:", farthest_points)

df = pd.read_excel('nsga2_result.xlsx')

best_configurations_nsga2 = {}

df_all_points = pd.DataFrame()
executions = [closest_point,farthest_points[0],farthest_points[1]]
for i, points in enumerate(executions):
    filtered_df = df[(df['MRR'] == points[0]) & (df['MOP'] == points[1])]
    df_all_points = pd.concat([df_all_points, filtered_df], ignore_index=True)
    best_configurations_nsga2[i] = filtered_df.to_dict()

df_all_points.to_csv('best_configurations_nsga2.csv', index=False)
df_all_points.to_excel('best_configurations_nsga2.xlsx', index=False)


with open('best_configurations_nsga2.json', "w") as json_file:
    json.dump(best_configurations_nsga2, json_file, indent=4)