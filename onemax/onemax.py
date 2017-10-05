import random
random.seed(64)

CHROMOSOME_SIZE = 10
GENE_MUTATION = 0.1
INDIVIDUAL_MUTATION = 0.1
POPULATION_SIZE = 100
ELITE_SIZE = 2
GENERATION_MAX = 30


class Individual:
    def __init__(self, chromosome, fitness=None):
        self.chromosome = chromosome
        self.fitness = fitness

    def mutate(self, mutation):
        for i in self.chromosome:
            if mutation > (random.randint(0, 100) / 100):
                self.chromosome[i] = random.randint(0, 1)

    def fit(self):
        self.fitness = sum(self.chromosome) / len(self.chromosome)


def create_individual(chromosome_size):
    return Individual([random.randint(0, 1) for i in range(chromosome_size)])


def select_individual(population, elite_size):
    population = sorted(population, reverse=True, key=lambda i: i.fitness)     
    elite = [population.pop(0) for i in range(elite_size)]
    random.shuffle(population)
    return elite, population


def crossover(a, b):
    # Two-point crossover
    a_chr = a.chromosome
    b_chr = b.chromosome
    
    size = len(a_chr)

    f = random.randint(0, size)
    s = random.randint(f, size)

    _a = a_chr[:f] + b_chr[f:s] + a_chr[s:]
    _b = b_chr[:f] + a_chr[f:s] + b_chr[s:]

    return [Individual(_a), Individual(_b)]


def mutate(population, individual_mutation, gene_mutation):
    for i in range(len(population)):
        if individual_mutation > (random.randint(0, 100) / 100):
            population[i].mutate(gene_mutation)
    return population


def main1():
    # Population of the first generation
    population = [create_individual(CHROMOSOME_SIZE) for i in range(POPULATION_SIZE)]
    
    # Start
    print("START\n", population[0].chromosome, "\n")
    
    for generation in range(GENERATION_MAX):

        # Fit
        [population[i].fit() for i in range(POPULATION_SIZE)]
        
        # Result
        result = [p.fitness for p in population]
        print("{0} Generation ---".format(generation + 1))
        print("\tMIN: {0}".format(min(result)))
        print("\tMAX: {0}".format(max(result)))
        print("\tAVG: {0}".format(round(sum(result) / len(result), 3)), "\n")

        # Select
        selected_individual, population = select_individual(population, ELITE_SIZE)
        
        # Crossover
        crossover_individual = []
        for i in range(len(population)-1):
            crossover_individual.extend(crossover(population[i], population[i+1]))
        random.shuffle(crossover_individual)

        # Mutate, Generate offspring
        offspring = mutate(crossover_individual[:POPULATION_SIZE-ELITE_SIZE], INDIVIDUAL_MUTATION, GENE_MUTATION)
        offspring.extend(selected_individual)

        # Update population
        population = offspring

    print("-"*30, "\nResult:")
    [print(selected_individual[i].chromosome) for i in range(len(selected_individual))]


def main2():
    # Population of the first generation
    population = [create_individual(CHROMOSOME_SIZE) for i in range(POPULATION_SIZE)]
    
    # Start
    print("START\n", population[0].chromosome, "\n")

    p_size = POPULATION_SIZE
    
    generation = 0
    while 1:
        generation += 1
             
        # Fit
        [population[i].fit() for i in range(p_size)]
        
        # Result
        result = [p.fitness for p in population]
        print("{0} Generation ---".format(generation))
        print("\tMIN: {0}".format(min(result)))
        print("\tMAX: {0}".format(max(result)))
        print("\tAVG: {0}".format(round(sum(result) / len(result), 3)), "\n")
        
        # Select
        selected_individual, population = select_individual(population, ELITE_SIZE)
        
        # Crossover
        crossover_individual = []
        for i in range(len(population)-1):
            crossover_individual.extend(crossover(population[i], population[i+1]))
        random.shuffle(crossover_individual)
        
        p_size -= ELITE_SIZE
        
        # Mutate, Generate offspring
        offspring = mutate(crossover_individual[:p_size], INDIVIDUAL_MUTATION, GENE_MUTATION)
        offspring.extend(selected_individual)

        # Update population
        population = offspring
        
        if len(population) <= ELITE_SIZE:
            break

    print("-"*30, "\nResult:")
    [print(population[i].chromosome) for i in range(len(population))]


if __name__ == '__main__':
    main1()
    main2()
    