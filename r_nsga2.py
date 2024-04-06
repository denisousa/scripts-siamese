import numpy as np
import statistics
from pymoo.algorithms.moo.rnsga2 import RNSGA2
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.pntx import SinglePointCrossover
from nsga2_mutation import MyMutation
from nsga2_problem import MyProblem
from nsga2_utils import print_results
import pandas as pd
import time

def compute_neighbor_ref_point(all_points, offset):
    all_mrr = [pareto_front[0] for pareto_front in all_points]
    all_mop = sorted([pareto_front[1] for pareto_front in all_points])

    median_mrr = statistics.median(all_mrr)
    median_mop = statistics.median(all_mop)
    
    point_1 = [max(all_mrr) + offset, median_mop + offset]
    point_2 = [median_mrr + offset, max(all_mop) + offset]
    point_3 = [max(all_mrr) + offset, max(all_mop) + offset]
    return [point_1, point_2, point_3]

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


def get_all_points(all_excel_path):
    all_points = []
    for excel_file_path in all_excel_path:
        pareto_front = calculate_pareto_front(excel_file_path, "MRR", "MOP")
        for point in pareto_front:
            all_points.append(point)
    return all_points

'''algorithm = NSGA2(pop_size=10,
                  sampling=IntegerRandomSampling(),
                  crossover=SinglePointCrossover(),
                  mutation=MyMutation(),
                  eliminate_duplicates=True)

problem = MyProblem()
result = minimize(problem,
               algorithm,
               get_termination("time", "54:10:49"), 
               seed=int(time.time()),
               verbose=True)'''


problem = get_problem("zdt1", n_var=30)
pf = problem.pareto_front()

all_excel_path = [
'grid_search_result.xlsx',
'random_search_result.xlsx',
'bayesian_search_result_05_05.xlsx',
'bayesian_search_result_07_03.xlsx',
'bayesian_search_result_03_07.xlsx',
'nsga2_result.xlsx'
]

all_points = get_all_points(all_excel_path)
ref_points = compute_neighbor_ref_point(all_points, 0.01)
ref_points = np.array(ref_points)

algorithm = RNSGA2(
    ref_points=ref_points,
    pop_size=10,
    epsilon=0.01,
    normalization='front',
    extreme_points_as_reference_points=False,
    sampling=IntegerRandomSampling(),
    crossover=SinglePointCrossover(),
    mutation=MyMutation(),
    eliminate_duplicates=True,
    weights=np.array([0.5, 0.5])
)

'''res = minimize(problem,
               algorithm,
               save_history=True,
               termination=('n_gen', 250),
               seed=1,
               pf=pf,
               disp=False)'''


'''
Posso dizer que o boxplot conseguiu explorar bem o MRR.

Nas 400 e poucas cofigurações tem MOP mt baixo e tem MOP muito alto.

O traço dentro da caixa representa a mediana.

Quanto maior a caixa, significa que ele explorou mais os dados.

Quando a mediana tá baixa, significa que os dados explorados foram ruins

O melhor algoritmo foi o Bayesian 0.5, 0.5

Devo mostra que o Bayesian é o mais eficiente, dada sua mediana estar acima do demais, e que boa parte de sua distribuição está alta.

Devo chamar de algoritmos tradicionais

Observação, percebemos uqe o 0,7 e 0,3 foi parecido.
Ele dá mais enfase para o MRR 

A caixa do 0.3, 0.7 já 

mais itneressante é falar que o Bayesian 0,5 e 0,5 é balanceada.

O Grid Search foi quem explorou melhor

Não devo falar sobre a otimização Bayesiana só com uma métrica

Boxplot representa a distribuição dos resultados que encontrei.

Usar baseline algorithmns ou São algoritmos de otimização traidicionais.

Adicionar na RQ1: Multi objetive clone parameter configuration,

RQ2: Como um algoritmo de otimização multi-objetiva se compara com algoritmos tradicionais, para o problema de XXXXXX.

Posso chamar de estudo piloto, experimento preliminar, o quue foi feito para os ngram
'''

'''
A gente deve falar das frentes paretos na primeira pergunta de pesquisa, só dos algoritmos tradicionais.

Posso falar mais claramente que os resultados do Grid é bom.

Para a segunda de pesquisa a gente compara só o NSGA-II com o Bayesian 0.5, 0.5

Tirar a tabela

Devo usar o nome "Search Algorithmns"

RQ1: Frentes de pareto dos tradicionais e boxplot

RQ2: Frente de pareto do NSGA-II e Bayesian 0.5, 0.5
'''