from generate_metrics import get_metrics

optimization_algorithms = [
    'nsga2',
    'grid_search',
    'random_search',
    'bayesian_search',
    'bayesian_search',
    'bayesian_search',
]

temp = [
    '2024-03-29 08:40:02.968719',
    '2024-04-01 10:13:13.495266',
    '2024-01-18 18:28:46.770455',
    'weighted_average_0.5_0.5',
    'weighted_average_0.7_0.3',
    'weighted_average_0.3_0.7',
]

get_metrics(optimization_algorithms, temp)
