

def percent_greater(num1, num2):
    if num2 == 0:
        return "Cannot calculate, as the second number is zero."
    
    difference = num1 - num2
    percentage = (difference / num2) * 100
    
    return f"{num1} is {percentage:.4f}% greater than {num2}."

default = {'mop': 0.4371, 'mrr': 0.6167}
midle = {'mop': 0.7366, 'mrr': 0.8681}
best_mop = {'mop': 0.7478, 'mrr': 0.5808}
best_mrr = {'mop': 0.0967, 'mrr': 0.9022}

print('Balance')
print('MRR', percent_greater(midle['mrr'], default['mrr']))
print('MOP', percent_greater(midle['mop'], default['mop']))
print()

print('Best MRR')
print('MRR', percent_greater(best_mrr['mrr'], default['mrr']))
print('MOP', percent_greater(best_mrr['mop'], default['mop']))
print()

print('Best MOP')
print('MRR', percent_greater(best_mop['mrr'], default['mrr']))
print('MOP', percent_greater(best_mop['mop'], default['mop']))
