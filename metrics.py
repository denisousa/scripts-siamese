import numpy as np

def calculate_ap(y_true, y_pred):
    sorted_indices = np.argsort(y_pred)[::-1]
    num_relevant = np.sum(y_true)
    
    precision_sum = 0
    tp = 0
    for i, idx in enumerate(sorted_indices):
        if y_true[idx] == 1:
            tp += 1
            precision = tp / (i + 1)
            precision_sum += precision
    
    if num_relevant == 0:
        return 0
    
    average_precision = precision_sum / num_relevant
    return average_precision

def calculate_map_at_k(y_true, y_pred, k):
    map_scores = []
    for i in range(len(y_true)):
        sorted_indices = np.argsort(y_pred[i])[::-1]
        k_sorted_indices = sorted_indices[:k]
        ap = calculate_ap(y_true[i][k_sorted_indices], y_pred[i][k_sorted_indices])
        map_scores.append(ap)
    
    mean_average_precision = np.mean(map_scores)
    return mean_average_precision

# Exemplo de resultados relevantes e resultados previstos para cada consulta
y_true = [[1, 0, 1, 0, 1],
          [0, 1, 1, 0, 0],
          [1, 1, 0, 0, 1]]
y_pred = [[0.8, 0.2, 0.6, 0.4, 0.7],
          [0.3, 0.5, 0.6, 0.2, 0.4],
          [0.9, 0.6, 0.3, 0.2, 0.8]]

# Definir o valor de K
k = 3

# Calcular o Mean Average Precision at K
map_at_k = calculate_map_at_k(y_true, y_pred, k)

# Exibir o resultado
print("Mean Average Precision at K (K={}):".format(k), map_at_k)
