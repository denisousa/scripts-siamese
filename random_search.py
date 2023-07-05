from itertools import product
import itertools
import random

def run_tool(X, Y):
    return random.randint(1, 10000), random.randint(1, 10000), random.randint(1, 10000)

# Stop when reaches 'num_iterations'
def evaluate_tool(x_values, y_values, num_iterations):
    best_score, best_X, best_Y = 0, 0, 0

    for _ in range(num_iterations):
        X = random.choice(x_values)
        Y = random.choice(y_values)
        
        recall, precision, f1_score = run_tool(X, Y)

        if f1_score > best_score:
            best_score, best_X, best_Y = f1_score, X, Y

    return best_X, best_Y

def execute_random_search():
    x_values, y_values, num_iterations = range(1,101), range(1,101), 50
    quantity_combinations = len(list(product(x_values, y_values)))
    best_X, best_Y = evaluate_tool(x_values, y_values, num_iterations)

    print("Melhores hiperparâmetros encontrados:")
    print("X:", best_X)
    print("Y:", best_Y)

execute_random_search()