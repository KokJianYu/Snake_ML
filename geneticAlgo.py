import numpy as np
import pandas as pd
import math
class GeneticAlgo:
    mutation_chance = 0.01
    global best_fitness
    best_fitness = 0
    global best_snake_model
    global fitness_file
    fitness_file = open("model/fitness.csv", "a")
    def generatePopulation(self, n_population, n_weights):
        population_flatten = np.random.choice(
            np.arange(-1, 1, 0.1), size=n_population * n_weights)
        return np.reshape(population_flatten, (n_population, n_weights))

    def updateBestSnake(self, current_population, population_fitness):
        global best_fitness
        global best_snake_model
        global fitness_file
        n_weights = np.asarray(current_population).shape[1]
        population_best_fitness_idx = np.argmax(population_fitness)
        if best_fitness < population_fitness[population_best_fitness_idx]:
            best_fitness = population_fitness[population_best_fitness_idx]
            best_snake_model = np.reshape(current_population[population_best_fitness_idx],(1, n_weights))
        df = pd.DataFrame(np.reshape(population_fitness[population_best_fitness_idx], (1, 1)))
        df.to_csv(fitness_file, header=None, index=None)

    def getNextGeneration(self, current_population, population_fitness, n_population=-1):
        n_weights = np.asarray(current_population).shape[1]
        if np.asarray(current_population).ndim == 1:
            print("Not enough parents to crossbreed")

        if n_population == -1:
            n_population = np.asarray(current_population).shape[0]

        global best_snake_model
        self.updateBestSnake(current_population, population_fitness)
        child_population = np.zeros((n_population, n_weights))
        child_population[0, :] = best_snake_model

        for i in range(1, n_population):
            parent1 = self.selectParent(current_population, population_fitness)
            parent2 = self.selectParent(current_population, population_fitness)
            child_population[i, :] = self.crossBreed(parent1, parent2)

        return self.mutation(child_population)

    def selectParent(self, current_population, population_fitness):
        total_fitness = math.floor(np.sum(population_fitness))
        chosen_fitness = np.random.randint(0, total_fitness, size=1)
        sum_fitness = 0
        for i in range(0, len(population_fitness)):
            sum_fitness += population_fitness[i]
            if(sum_fitness > chosen_fitness):
                return current_population[i]

    def crossBreed(self, parent1, parent2):
        mating_pair = np.vstack((parent1, parent2))
        selected_parents = np.random.choice(range(0, 1), size=len(parent1), replace=True)
        return [mating_pair[selected_parents[i], [i]] for i in range(0, len(parent1))]

    def mutation(self, child_population):
        n_child_population = child_population.shape[0]
        n_child_weights = child_population.shape[1]
        num_of_mutation = int((n_child_population * n_child_weights) // (self.mutation_chance ** -1))

        #Do not mutate first child!
        x = np.random.choice(range(1, n_child_population), num_of_mutation, replace=True)
        y = np.random.choice(range(0, n_child_weights), num_of_mutation, replace=True)
        for i in range(0, num_of_mutation):
            mutation = np.random.normal(0, 1, size=1)
            child_population[x[i], y[i]] = mutation
            #print(f"{x[i]},{y[i]} mutated by {mutation}")
        return child_population


class MainStub: 

    def runTest(self):
        genes = GeneticAlgo()
        n_pop = 4
        n_weight = 20
        init_population = genes.generatePopulation(n_pop, n_weight)
        print(init_population)
        fitness = np.random.rand(n_pop)*500000
        nextGen = genes.getNextGeneration(init_population, fitness)
        print("Next Gen")
        print(nextGen)


def main():
    MainStub().runTest()


if __name__ == "__main__":
    main()