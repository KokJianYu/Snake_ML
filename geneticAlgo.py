import numpy as np


class GeneticAlgo:
    mutation_chance = 0.1

    def generatePopulation(self, n_population, n_weights):
        population_flatten = np.random.choice(
            np.arange(-1, 1, 0.1), size=n_population * n_weights)
        return np.reshape(population_flatten, (n_population, n_weights))

    def getNextGeneration(self, current_population, population_fitness, n_population=-1):
        if np.asarray(current_population).ndim == 1:
            print("Not enough parents to crossbreed")

        if n_population == -1:
            n_population = np.asarray(current_population).shape[0]

        mating_pool = self.getMatingPool(
            current_population, population_fitness)
        return self.crossBreedMatingPopulation(mating_pool, n_population)

    def getMatingPool(self, current_population, population_fitness, num_parents=-1):
        n_population = np.asarray(current_population).shape[0]
        if num_parents == -1:
            num_parents = n_population // 10
            num_parents = num_parents if num_parents > 1 else 2

        mating_pool_idxs = np.argpartition(population_fitness, -num_parents)[-num_parents:]
        return current_population[mating_pool_idxs]

    def crossBreedMatingPopulation(self, mating_population, n_population):
        if np.asarray(mating_population).ndim == 1:
            print("Not enough parents to crossbreed")
        
        n_mating_population = mating_population.shape[0]
        n_weights = np.asarray(mating_population).shape[1]

        child_population = np.empty((n_population, n_weights))
        for i in range(0, n_population):
            crossbreeding_parents_id = np.random.choice(
                range(0, n_mating_population), size=2, replace=False)
            selected_parents = np.random.choice(
                crossbreeding_parents_id, size=n_weights, replace=True)
            child_weights = [mating_population[selected_parents[i], [i]] for i in range(0, n_weights)]
            child_population[i, :] = child_weights
        child_population = self.mutation(child_population)
        return child_population

    def mutation(self, child_population):
        n_child_population = child_population.shape[0]
        n_child_weights = child_population.shape[1]
        num_of_mutation = int(n_child_population // (self.mutation_chance ** -1))

        x = np.random.choice(range(0, n_child_population), num_of_mutation, replace=True)
        y = np.random.choice(range(0, n_child_weights), num_of_mutation, replace=True)
        for i in range(0, num_of_mutation):
            mutation = np.random.choice(np.arange(-1, 1, 0.01))
            child_population[x[i], y[i]] += mutation
            print(f"{x[i]},{y[i]} mutated by {mutation}")
        return child_population


class MainStub: 
    genes = GeneticAlgo()
    n_pop = 10
    n_weight = 10
    init_population = genes.generatePopulation(n_pop, n_weight)
    fitness = np.random.rand(10)
    nextGen = genes.getNextGeneration(init_population, fitness)
    print("Next Gen")
    print(nextGen)


MainStub()