import random
from deap import base, creator, tools

# Definindo o problema de otimização
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Definindo os hiperparâmetros disponíveis
ngram_values = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
minclonesize_values = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
qrpercentile_values = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
boost_values = [-1, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
simthreshold_values = [
    '10%,20%,30%,40%',
    '20%,30%,40%,50%',
    '30%,40%,50%,60%',
    '40%,50%,60%,70%',
    '50%,60%,70%,80%',
    '60%,70%,80%,90%',
    '10%,30%,40%,50%',
    '20%,40%,60%,70%',
    '30%,60%,80%,90%',
]

# Criando a caixa de ferramentas
toolbox = base.Toolbox()
toolbox.register("attr_ngram", random.choice, ngram_values)
toolbox.register("attr_minclonesize", random.choice, minclonesize_values)
toolbox.register("attr_qrpercentile", random.choice, qrpercentile_values)
toolbox.register("attr_boost", random.choice, boost_values)
toolbox.register("attr_simthreshold", random.choice, simthreshold_values)

# Criando um indivíduo
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_ngram, toolbox.attr_minclonesize, toolbox.attr_qrpercentile,
                  toolbox.attr_boost, toolbox.attr_simthreshold), n=1)

# Criando a população
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Definindo a função de avaliação (MRR)
def evaluate(individual):
    # Substitua esta função pela lógica de execução do Siamese e cálculo do MRR
    # Aqui, estamos usando uma função de avaliação fictícia
    mrr_score = random.uniform(0, 1)
    return mrr_score,

toolbox.register("evaluate", evaluate)

# Definindo os operadores genéticos
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Configurando a população e número de gerações
population_size = 10
generations = 5
population = toolbox.population(n=population_size)

# Avaliando toda a população
fitnesses = list(map(toolbox.evaluate, population))
for ind, fit in zip(population, fitnesses):
    ind.fitness.values = fit

# Evolução da população
for gen in range(generations):
    # Seleção
    offspring = toolbox.select(population, len(population))
    offspring = list(map(toolbox.clone, offspring))

    # Cruzamento e mutação
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.9:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < 0.1:
            print(mutant)
            toolbox.mutate(mutant)
            print(mutant)
            print()
            del mutant.fitness.values

    # Avaliação
    fitnesses = list(map(toolbox.evaluate, offspring))
    for ind, fit in zip(offspring, fitnesses):
        ind.fitness.values = fit

    # Substituindo a população antiga pela nova
    population[:] = offspring

    # Melhor indivíduo da geração
    best_ind = tools.selBest(population, 1)[0]
    print(f"Generation {gen}: Best MRR {best_ind.fitness.values[0]}")

# Obtendo a melhor solução após a evolução
best_ind = tools.selBest(population, 1)[0]
print("Best Individual:", best_ind)
print("Best MRR:", best_ind.fitness.values[0])
