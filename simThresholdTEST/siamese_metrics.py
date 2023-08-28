import numpy as np


def precision_at_k(recommended_items, relevant_items, k):
    recommended_and_relevant = [item for item in recommended_items[:k] if item in relevant_items]
    return len(recommended_and_relevant) / k


def recall_at_k(recommended_items, relevant_items, k):
    recommended_and_relevant = [item for item in recommended_items[:k] if item in relevant_items]
    return len(recommended_and_relevant) / len(relevant_items)


def apk(recommended_items, relevant_items, k):
    if len(recommended_items)>k:
        recommended_items = recommended_items[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(recommended_items):
        if p in relevant_items and p not in recommended_items[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if not relevant_items:
        return 0.0

    return score / min(len(relevant_items), k)


def mapk(recommended_items, relevant_items, k):
    return np.mean([apk(a,p,k) for a,p in zip(recommended_items, relevant_items)])


recommended_items = [1, 0, 2, 10, 3, 8, 4]
relevant_items = [1, 2, 3, 4]

k = 5
precision_at_k_value = precision_at_k(recommended_items, relevant_items, k)
recall_at_k_value = recall_at_k(recommended_items, relevant_items, k)
average_precisions_value = apk(recommended_items, relevant_items, k)

print(f"Precision@{k} = {precision_at_k_value:.2f}")
print(f"Recall@{k} = {recall_at_k_value:.2f}")
print(f"Average Precisions: {average_precisions_value}")


# in this case we need more than one list of recommendation and items of wanted items
recommended_items = [[1, 0, 2, 10, 3, 8, 4], [1, 2, 3]]
relevant_items = [[1, 2, 3, 4], [0, 3, 7]]

mean_average_precision_value = mapk(recommended_items, relevant_items, k)
print(f"Mean Average Precision: {mean_average_precision_value:.2f}")