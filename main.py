import keras
import snakeML
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import pandas as pd
import geneticAlgo


def getPopulationFromCsv():
    df = pd.read_csv("nextpopulation.csv", sep=',', header=None)
    return np.asarray(df.values)


def reshapeWeights(weights, input_layer_units, hidden_layers_units, output_layer_units):

    firstIndex = 0
    lastIndex = (input_layer_units * hidden_layers_units[0])
    weight_1 = np.reshape(
        weights[firstIndex:lastIndex], (input_layer_units, hidden_layers_units[0]))
    activation_1 = np.zeros(9)  # np.asarray([stackedWeights, np.zeros(9)])
    firstIndex = lastIndex
    lastIndex = firstIndex + (hidden_layers_units[0] * hidden_layers_units[1])
    weight_2 = np.reshape(
        weights[firstIndex:lastIndex], (hidden_layers_units[0], hidden_layers_units[1]))
    activation_2 = np.zeros(15)  # np.asarray([stackedWeights, np.zeros(15)])
    firstIndex = lastIndex
    lastIndex = firstIndex + (hidden_layers_units[1] * output_layer_units)
    weight_3 = np.reshape(
        weights[firstIndex:lastIndex], (hidden_layers_units[1], output_layer_units))
    activation_3 = np.zeros(3)  # np.asarray([stackedWeights, np.zeros(3)])
    return np.array([weight_1, activation_1, weight_2, activation_2, weight_3, activation_3])


GeneticAlgo = geneticAlgo.GeneticAlgo()
num_of_gens = 100
n_population = 100
max_steps = 2000

# Build model (Building fixed NN first)
input_layer_units = 7
hidden_layers_units = [9, 15]
output_layer_units = 3
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(
    hidden_layers_units[0], input_dim=input_layer_units, activation=tf.nn.sigmoid))
model.add(tf.keras.layers.Dense(
    hidden_layers_units[1], activation=tf.nn.sigmoid))
model.add(tf.keras.layers.Dense(output_layer_units, activation=tf.nn.softmax))
total_weights = input_layer_units * hidden_layers_units[0]
total_weights += hidden_layers_units[0] * hidden_layers_units[1]
total_weights += hidden_layers_units[1] * output_layer_units

# Genetic loop
population = GeneticAlgo.generatePopulation(
    n_population, total_weights)  # Change to total number of weights
#population = getPopulationFromCsv()
for i in range(0, num_of_gens):
    print(f"Generation {i}:")
    fitness = np.empty(n_population)
    for j in range(0, n_population):
        weights = reshapeWeights(
            population[j], input_layer_units, hidden_layers_units, output_layer_units)
        model.set_weights(weights)
        snakeML.newGameML()
        snakeML.startGameML()
        game_ended = False
        num_steps = 0
        while not game_ended and (num_steps < max_steps):
            input_layer = snakeML.getInputLayer()
            output = model.predict(np.matrix(input_layer))
            # predict output
            output = np.argmax(output)
            fitness[j], game_ended = snakeML.nextStep(output)
            num_steps += 1
        snakeML.exit()
        print(f"Population {j+1} completed. Fitness = {fitness[j]}")
    # Print out stats here
    best_person = np.argmax(fitness)
    print(f"Generation {i}, Top fitness = {fitness[best_person]}")

    weights = reshapeWeights(
        population[best_person], input_layer_units, hidden_layers_units, output_layer_units)
    model.set_weights(weights)
    model.save(f"model_generation_{i}_best_fitness")
    print(f"Generation {i} best model saved.")
    population = GeneticAlgo.getNextGeneration(population, fitness)
    df = pd.DataFrame(population)
    df.to_csv('nextpopulation.csv', header=None, index=None)
