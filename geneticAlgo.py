import numpy as np
import pandas as pd
import math
import random

class GeneticAlgo:
    #Parameters for genetic algo
    mutation_rate = 0.01
    snake_to_retain = 5
    global best_fitnesses
    best_fitnesses = np.empty(1)
    global best_snake_models
    def generatePopulation(self, n_population, n_weights):
        global best_snake_models
        best_snake_models = np.empty(n_weights)
        population_flatten = np.random.choice(
            np.arange(-1, 1, 0.1), size=n_population * n_weights)
        return np.reshape(population_flatten, (n_population, n_weights))

    def updateBestSnakes(self, current_population, population_fitness):
        global best_fitnesses
        global best_snake_models
        if(len(population_fitness) < self.snake_to_retain):
            self.snake_to_retain = len(population_fitness)
        n_weights = np.asarray(current_population).shape[1]
        population_best_fitnesses_idx = np.argpartition(population_fitness, -self.snake_to_retain)[-self.snake_to_retain:]
        for i in range(self.snake_to_retain):
            best_fitnesses = np.append(best_fitnesses, population_fitness[population_best_fitnesses_idx[i]])
            best_snake_models = np.vstack((best_snake_models, np.reshape(current_population[population_best_fitnesses_idx[i]],(1, n_weights))))

        best_fitnesses_idx = np.argpartition(best_fitnesses, -self.snake_to_retain)[-self.snake_to_retain:]
        best_fitnesses = best_fitnesses[best_fitnesses_idx]
        best_snake_models = best_snake_models[best_fitnesses_idx]


    def getNextGeneration(self, current_population, population_fitness, n_population=-1):
        n_weights = np.asarray(current_population).shape[1]
        if np.asarray(current_population).ndim == 1:
            print("Not enough parents to crossbreed")

        if n_population == -1:
            n_population = np.asarray(current_population).shape[0]

        global best_snake_models
        self.updateBestSnakes(current_population, population_fitness)
        child_population = np.zeros((n_population, n_weights))
        # Bring the best few snakes to the next population, without getting mutated
        for i in range(self.snake_to_retain):
            child_population[i, :] = best_snake_models[i]

        for i in range(self.snake_to_retain, n_population):
            parent1 = self.selectParent(current_population, population_fitness)
            parent2 = self.selectParent(current_population, population_fitness)
            child_population[i, :] = self.crossBreed(parent1, parent2)

        return self.mutation(child_population)

    # Randomly select a parent from current population based on fitness level.
    # Higher fitness level --> Higher chance of getting selected
    def selectParent(self, current_population, population_fitness):
        total_fitness = math.floor(np.sum(population_fitness))
        chosen_fitness = random.randint(0, total_fitness)
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
        
        for i in range(1, n_child_population):
            for j in range(0, n_child_weights):
                if np.random.random_sample() < self.mutation_rate:
                    mutation = np.random.normal(0, 1, size=1)
                    child_population[i, j] = mutation
        return child_population


#This class is used to test the methods in this class
class MainStub: 

    def runTest(self):
        genes = GeneticAlgo()
        n_pop = 10
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