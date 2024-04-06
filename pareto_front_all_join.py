import pandas as pd
import matplotlib.pyplot as plt
import os

excel_file_path_list = [
#'grid_search_result.xlsx',
'random_search_result.xlsx',
'bayesian_search_result_05_05.xlsx',
'bayesian_search_result_07_03.xlsx',
'bayesian_search_result_03_07.xlsx',
]

labels = [
#'Grid Search',
'Random Search',
'Bayesian Search (0.5, 0.5)',
'Bayesian Search (0.7, 0.3)',
'Bayesian Search (0.3, 0.7)',
]


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
    plt.plot(*zip(*pareto_front), label=labels[index_excel])
    # plt.title('Pareto Front')
    plt.xlabel('Mean Reciprocal Rank - MRR')
    plt.ylabel('Mean Overall Precision - MOP')
    plt.legend()
    plt.grid(True)
    plt.savefig("pareto_front")

plt.show()