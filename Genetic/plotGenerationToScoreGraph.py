import keras
import snakeML
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# This class is used to plot out the performance of each snake generation trained by genetic algorithm

SIZE_INPUT_LAYER = 14
# Model is hard coded. Change here if you modified it in main.py
model = keras.Sequential()
model.add(keras.layers.Dense(30, activation="relu", input_dim=SIZE_INPUT_LAYER))
model.add(keras.layers.Dense(30, activation="relu"))
model.add(keras.layers.Dense(30, activation="relu"))
model.add(keras.layers.Dense(3, activation="softmax"))
# Don't actually need compile model since we are not training anything
opt = keras.optimizers.Adam(0.0005)
model.compile(loss="mse", optimizer=opt)

PATH = f"model/"
GAMES_PER_GENERATION = 10
SHOW_GUI = False
files = os.listdir(PATH)
score_plot = []
generation_plot = []
for i in range(len(files)):
    weightsToUse = f"{PATH}{files[i]}"
    model.load_weights(weightsToUse)
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
    episodes = np.array(array_counter)
    scores = np.array(array_score)
    z = np.polyfit(episodes, scores, 3)
    p = np.poly1d(z)
    scores_new = p(episodes)
    plt.plot(episodes, scores, 'o', episodes, scores_new)
    plt.show()


plot_seaborn(generation_plot, score_plot)
