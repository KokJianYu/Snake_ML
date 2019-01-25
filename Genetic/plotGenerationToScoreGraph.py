from tensorflow import keras
import snakeML
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# This class is used to plot out the performance of each snake generation trained by genetic algorithm

SIZE_INPUT_LAYER = 14

PATH = f"model/"
GAMES_PER_GENERATION = 10
SHOW_GUI = False
files = os.listdir(PATH)
score_plot = []
generation_plot = []
for i in range(len(files)):
    weightsToUse = f"{PATH}{files[i]}"
    model = keras.models.load_model(weightsToUse)
    totalScore = 0
    for j in range(GAMES_PER_GENERATION):
        score = 0
        counter = 0
        snakeML.newGameML()
        snakeML.startGameML(showGui=SHOW_GUI)
        while not snakeML.gameEnded and counter < 200:
            state = np.reshape(snakeML.getInputLayer(), (1, SIZE_INPUT_LAYER))
            output = model.predict(state)
            action = np.argmax(output)
            snakeML.nextStep(action)
            if(score == snakeML.snake.length - 1):
                counter += 1
            else:
                score = snakeML.snake.length - 1
                counter = 0
        totalScore += score
        snakeML.exit()
    score_plot.append(totalScore / GAMES_PER_GENERATION)
    generation_plot.append(i)
    print(f"File={files[i]} Score={totalScore / GAMES_PER_GENERATION}")


def plot_seaborn(array_counter, array_score):
    generation = np.array(array_counter)
    scores = np.array(array_score)
    z = np.polyfit(generation, scores, 3)
    p = np.poly1d(z)
    scores_new = p(generation)
    plt.xlabel("Generation")
    plt.ylabel("Score")
    plt.plot(generation, scores, 'o', generation, scores_new)
    plt.show()


plot_seaborn(generation_plot, score_plot)
