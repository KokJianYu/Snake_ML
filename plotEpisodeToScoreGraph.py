import keras
import snakeML
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

SIZE_INPUT_LAYER = 14
#Model is hardcoded. Change to be identical to model in DeepQNetwork.py
model = keras.Sequential()
model.add(keras.layers.Dense(30, activation="relu", input_dim=SIZE_INPUT_LAYER))
model.add(keras.layers.Dropout(0.15))
model.add(keras.layers.Dense(30, activation="relu"))
model.add(keras.layers.Dropout(0.15))
model.add(keras.layers.Dense(30, activation="relu"))
model.add(keras.layers.Dropout(0.15))
model.add(keras.layers.Dense(3, activation="softmax"))
opt = keras.optimizers.Adam(0.01)
model.compile(loss="mse", optimizer=opt)

PATH = f"model/"
GAMES_PER_EPISODE = 10
SHOW_GUI = False
files = os.listdir(PATH)
score_plot = []
episode_plot = []
for i in range(len(files)):
    weightsToUse = f"{PATH}{files[i]}"
    model.load_weights(weightsToUse)
    totalScore = 0
    for j in range(GAMES_PER_EPISODE):
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
    score_plot.append(totalScore / GAMES_PER_EPISODE)
    episode_plot.append(i * 10) 
    print(f"File={files[i]} Score={totalScore / GAMES_PER_EPISODE}")

def plot_seaborn(array_counter, array_score):
    episodes = np.array(array_counter)
    scores = np.array(array_score)
    z = np.polyfit(episodes, scores, 3)
    p = np.poly1d(z)
    scores_new = p(episodes)
    plt.plot(episodes, scores, 'o', episodes, scores_new)
    plt.show()
    # data = {"episodes": episodes, "scores": scores}
    # df = pd.DataFrame(data)
    # sns.set(color_codes=True)
    # sns.lineplot(x="episodes", y="scores", data=df)
    # plt.show()


plot_seaborn(episode_plot, score_plot)