'''
NOTE: Only Works with pip install "numpy<1.24.0"
'''

from skopt import gp_minimize
from skopt.space import Integer, Categorical
from skopt.utils import use_named_args
from siamese_search import execute_siamese_search

dimensions=[Integer(4, 24, name='ngramSize'),
            Integer(6, 10, name='minCloneSize'),
            Integer(1, 20, name='QRPercentileNorm'), 
            Integer(1, 20, name='QRPercentileT2'),
            Integer(1, 20, name='QRPercentileT1'),
            Integer(1, 20, name='QRPercentileOrig'),
            Categorical([-1, 1, 4, 10], name='normBoost'),
            Categorical([-1, 1, 4, 10], name='t2Boost'),
            Categorical([-1, 1, 4, 10], name='t1Boost'),
            Categorical([-1, 1, 4, 10], name='origBoost')]

@use_named_args(dimensions)
def evaluate_tool(**parms):
    parms['config_folder'] = 'configurations_bayesian_optimization'
    recall, precision, f1_score = execute_siamese_search(**parms)
    check.append({'recall': recall, 'precision': precision, 'f1_score': f1_score, 'parms': parms})
    loss = -f1_score

    return loss

def prove_algorithm(check):
    max_score, max_x, max_y = 0,0,0
    for score, x, y in check:
        if score > max_score:
            max_score, max_x, max_y = score, x, y

    print(max_score, max_x, max_y)

check = []

# Calls Bayesian Optimization
result = gp_minimize(evaluate_tool, dimensions=dimensions, n_calls=20, random_state=42)

print("Melhores hiperparâmetros encontrados:")
print("Hiperparâmetros: ", result)

prove_algorithm(check)
