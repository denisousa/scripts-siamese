from sklearn.metrics import average_precision_score
import numpy as np


def precision_at_k(recommended_items, relevant_items, k):
    recommended_and_relevant = [item for item in recommended_items[:k] if item in relevant_items]
    return len(recommended_and_relevant) / k


def recall_at_k(recommended_items, relevant_items, k):
    recommended_and_relevant = [item for item in recommended_items[:k] if item in relevant_items]
    return len(recommended_and_relevant) / len(relevant_items)


def apk(recommended_items, relevant_items, k):
    precisions = [precision_at_k(recommended_items, relevant_items, i) for i in range(1, k)]

    return sum(precisions)/ k


def mapk(recommended_items, relevant_items, k):
    return np.mean([apk(a,p,k) for a,p in zip(recommended_items, relevant_items)])


recommended_items = [1, 2, 0, 12, 13, 3]
relevant_items = [1, 2, 3, 4, 5, 6]

k = 3
precision_at_k_value = precision_at_k(recommended_items, relevant_items, k)
recall_at_k_value = recall_at_k(recommended_items, relevant_items, k)
average_precisions_value = apk(recommended_items, relevant_items, k)

print(f"Precision@{k} = {precision_at_k_value:.2f}")
print(f"Recall@{k} = {recall_at_k_value:.2f}")
print(f"Average Precisions: {average_precisions_value}")

recommended_items = [[1, 0, 2, 10, 3, 8, 4], [1, 2, 3]]
relevant_items = [[1, 2, 3, 4], [0, 3, 7]]

mean_average_precision_value = mapk(recommended_items, relevant_items, k)
print(f"Mean Average Precision: {mean_average_precision_value:.2f}")