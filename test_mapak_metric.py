def calculate_average_precision_at_k(actual, predicted, k):
    relevant_count = 0
    precision_sum = 0.0

    for i in range(k):
        if predicted[i] in actual:
            relevant_count += 1
            precision_at_i = relevant_count / (i + 1)
            precision_sum += precision_at_i

    if relevant_count == 0:
        return 0.0
    
    average_precision = precision_sum / min(k, len(actual))
    return average_precision

def calculate_map_at_k(actual_list, predicted_list, k):
    total_average_precision = 0.0
    
    for actual, predicted in zip(actual_list, predicted_list):
        ap_at_k = calculate_average_precision_at_k(actual, predicted, k)
        total_average_precision += ap_at_k
    
    map_at_k = total_average_precision / len(actual_list)
    return map_at_k

# Exemplo de dados
actual_list = [[1, 2, 3], [1, 4], [2, 4, 5]]
predicted_list = [[1, 3, 5], [1, 2, 4], [1, 3, 4]]

k = 2
map_at_k = calculate_map_at_k(actual_list, predicted_list, k)
print(f"MAP@{k} = {map_at_k:.4f}")
