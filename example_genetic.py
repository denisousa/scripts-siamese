import random

# Função a ser otimizada
def fitness_function(x):
    return -x**2 + 4*x

# Função de inicialização da população
def initialize_population(population_size):
    return [random.uniform(0, 4) for _ in range(population_size)]

# Avaliação da aptidão (fitness) de cada indivíduo na população
def evaluate_population(population):
    return [fitness_function(individual) for individual in population]

# Seleção de pais com base na roleta viciada pela aptidão
def select_parents(population, fitness_values):
    total_fitness = sum(fitness_values)
    probabilities = [fitness / total_fitness for fitness in fitness_values]
    parents = random.choices(population, weights=probabilities, k=2)
    return parents

# Crossover (média aritmética) para produzir descendentes
def crossover(parents):
    return sum(parents) / 2

# Mutação com pequenas alterações aleatórias
def mutate(child):
    mutation_rate = 0.1
    if random.random() < mutation_rate:
        return child + random.uniform(-0.5, 0.5)
    else:
        return child

# Algoritmo Genético
def genetic_algorithm(population_size, generations):
    population = initialize_population(population_size)

    for generation in range(generations):
        fitness_values = evaluate_population(population)

        new_population = []
        for _ in range(population_size // 2):
            parents = select_parents(population, fitness_values)
            child = crossover(parents)
            child = mutate(child)
            new_population.extend([child, mutate(child)])

        population = new_population

    best_solution = max(population, key=fitness_function)
    return best_solution, fitness_function(best_solution)

# Parâmetros do algoritmo
population_size = 10
generations = 50

# Executar o algoritmo genético
best_solution, best_fitness = genetic_algorithm(population_size, generations)

# Exibir resultado
print(f"Melhor solução: x = {best_solution}, Fitness = {best_fitness}")

'''
Solução|Indivíduo: Combinação de Hiperparâmetros


1. Vou gerar uma população: Um conjunto de soluções
2. Vou calcular o fitness da minha população
LOOP
3. Selecionar dois Indívudos
4. Crossover
5. Mutação
6. Gerar nova população agrupando os novos indívudos
'''