import keras
import snakeML
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import pandas as pd
import geneticAlgo
import math
import tkinter


def updateCanvas(txtbox_id, generation, n_snake, fitness, length, steps):
    scoreScreenCanvas.itemconfig(
        txtbox_id, text=f"Generation: {generation}, Snake: {n_snake}, Fitness: {fitness}, Length: {length}, Steps:{steps}")
    scoreScreenCanvas.update()


def getPopulationFromCsv(generation):
    df = pd.read_csv(
        f"generationInfo/generation{generation}.csv", sep=',', header=None)
    return np.asarray(df.values)


def reshapeWeights(population, input_layer_units, hidden_layers_units, output_layer_units):
    weights = []
    firstIndex = 0
    lastIndex = (input_layer_units * hidden_layers_units[0])
    weights.append(np.reshape(
        population[firstIndex:lastIndex], (input_layer_units, hidden_layers_units[0])))
    # np.asarray([stackedWeights, np.zeros(9)])
    weights.append(np.zeros(hidden_layers_units[0]))

    for i in range(0, hidden_layers_units.__len__()-1):
        firstIndex = lastIndex
        lastIndex = firstIndex + \
            (hidden_layers_units[i] * hidden_layers_units[i+1])
        weights.append(np.reshape(
            population[firstIndex:lastIndex], (hidden_layers_units[i], hidden_layers_units[i+1])))
        # np.asarray([stackedWeights, np.zeros(3)])
        weights.append(np.zeros(hidden_layers_units[1]))

    firstIndex = lastIndex
    lastIndex = firstIndex + (hidden_layers_units[-1] * output_layer_units)
    weights.append(np.reshape(
        population[firstIndex:lastIndex], (hidden_layers_units[-1], output_layer_units)))
    # np.asarray([stackedWeights, np.zeros(3)])
    weights.append(np.zeros(output_layer_units))
    return np.array(weights)

# Fitness function inspired from https://github.com/Code-Bullet/SnakeFusion


def calcFitness(len, num_steps):
    fitness = 0
    if len < 10:
        fitness = num_steps * num_steps * math.pow(2, len)
    else:
        fitness = num_steps * num_steps
        fitness *= math.pow(2, 10)
        fitness *= (len-9)

    return fitness


def buildModel(input_layer_units, hidden_layers_units, output_layer_units):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(
        hidden_layers_units[0], activation="relu", input_dim=input_layer_units))
    for i in range(1, len(hidden_layers_units)):
        model.add(tf.keras.layers.Dense(
            hidden_layers_units[i], activation="relu"))
    model.add(tf.keras.layers.Dense(output_layer_units, activation="softmax"))
    return model

################################### RUNNING CODE######################################################


# Set to true if you want to resume stopped training.
isResumeTraining = False
generationToResumeFrom = 0

# Set up UI for running genetic Algo
scoreScreenMaster = tkinter.Tk()
scoreScreenCanvas = tkinter.Canvas(
    scoreScreenMaster, bg="white", height=200, width=500)
scoreScreenCanvas.pack()
txtbox_trained_id = scoreScreenCanvas.create_text(
    250, 20, text=f"Generation: 0, Snake: 0, Fitness: 0, Length: 0")
txtbox_training_id = scoreScreenCanvas.create_text(
    250, 120, text=f"Generation: 0, Snake: 0, Fitness: training")

# Parameters for genetic algo
GeneticAlgo = geneticAlgo.GeneticAlgo()
num_of_gens = 100
n_population = 2000
# Increase max steps after every generation
max_steps = 200 + generationToResumeFrom * 20

# Build model
input_layer_units = 14
hidden_layers_units = [30, 30, 30]
output_layer_units = 3
model = buildModel(input_layer_units, hidden_layers_units, output_layer_units)
total_weights = input_layer_units * hidden_layers_units[0]
for i in range(0, len(hidden_layers_units) - 1):
    total_weights += hidden_layers_units[i] * hidden_layers_units[i+1]
total_weights += hidden_layers_units[-1] * output_layer_units

# Genetic loop
population = GeneticAlgo.generatePopulation(
    n_population, total_weights)
if isResumeTraining:
    population = getPopulationFromCsv(generationToResumeFrom)
# Loop for generations
for i in range(generationToResumeFrom, num_of_gens):
    print(f"Generation {i}:")
    fitness = np.empty(n_population)
    len = np.empty(n_population)
    steps = np.empty(n_population)
    # Loop for populations in a generation
    for j in range(0, n_population):
        weights = reshapeWeights(
            population[j], input_layer_units, hidden_layers_units, output_layer_units)
        model.set_weights(weights)
        snakeML.newGameML()
        snakeML.startGameML(showGui=False)
        game_ended = False
        num_steps = 0
        while not game_ended and (num_steps < max_steps):
            input_layer = snakeML.getInputLayer()
            output = model.predict(np.matrix(input_layer))
            output = np.argmax(output)
            foodEaten, game_ended = snakeML.nextStep(output)
            len[j] = snakeML.getSnakeLength()
            num_steps += 1
        steps[j] = num_steps
        fitness[j] = calcFitness(len[j], steps[j])
        snakeML.exit()
        updateCanvas(txtbox_training_id, i, j, fitness[j], len[j], steps[j])
    best_person = np.argmax(fitness)
    print(
        f"Generation {i}, Top fitness = {fitness[best_person]}, Length = {len[best_person]}, Steps = {steps[best_person]}")
    updateCanvas(txtbox_trained_id, i, "Null",
                 fitness[best_person], len[best_person], steps[best_person])

    weights = reshapeWeights(
        population[best_person], input_layer_units, hidden_layers_units, output_layer_units)
    model.set_weights(weights)
    model.save(f"model/model_generation_{i:02d}_best_fitness.hdf5")
    print(f"Generation {i} best model saved.")
    print("Creating next generation. This might take a while.")
    population = GeneticAlgo.getNextGeneration(population, fitness)
    
    # Saving data to allow for training to be resumed after being stopped
    df = pd.DataFrame(population)
    df.to_csv(
        f'generationInfo/generation{i+1:02d}.csv', header=None, index=None)

    # Increase max steps after every generation
    max_steps += 20
