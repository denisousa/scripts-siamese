def precision_at_k(y_true, y_scores, k):
    sorted_indices = sorted(range(len(y_scores)), key=lambda i: y_scores[i], reverse=True)
    y_true_sorted = [y_true[i] for i in sorted_indices]
    
    num_relevant = sum(y_true_sorted[:k])
    precision = num_relevant / k
    
    return precision

def average_precision_at_k(y_true, y_scores, k):
    total_precision = 0.0
    num_relevant = sum(y_true)
    
    for i in range(k):
        if y_true[i] == 1:
            precision_at_i = precision_at_k(y_true[:i+1], y_scores[:i+1], i+1)
            total_precision += precision_at_i
    
    avg_precision = total_precision / num_relevant
    
    return avg_precision

y_true = [1, 0, 1, 1, 0, 1]
y_scores = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4]

k = 3
precision_at_k_value = precision_at_k(y_true, y_scores, k)
avg_precision_at_k_value = average_precision_at_k(y_true, y_scores, k)

print(f"Precision@{k} = {precision_at_k_value:.4f}")
print(f"Average Precision@{k} = {avg_precision_at_k_value:.4f}")
