from tensorflow import keras
import numpy as np
import pandas as pd
import random

SIZE_INPUT_LAYER = 14

class DeepQNetworkAgent(object):

    def __init__(self):
        self.learningRate = 0.0005
        self.model = self.createModel()
        self.explorationEpsilon = 1
        self.epsilonDecay = 0.01
        self.memory = [] #Used to store [oldState, action, reward, newState, gameEnded]
        self.reward = 0
        self.discount = 0.85


    def explorationEpsilonDecay(self):
        self.explorationEpsilon -= self.epsilonDecay
        if(self.explorationEpsilon < 0.01):
            self.explorationEpsilon = 0.01

    def createModel(self, weights=None):
        model = keras.Sequential()
        model.add(keras.layers.Dense(30, activation="relu", input_dim=SIZE_INPUT_LAYER))
        #model.add(keras.layers.Dropout(0.15))
        model.add(keras.layers.Dense(30, activation="relu"))
        #model.add(keras.layers.Dropout(0.15))
        model.add(keras.layers.Dense(30, activation="relu"))
       # model.add(keras.layers.Dropout(0.15))
        model.add(keras.layers.Dense(3))
        opt = keras.optimizers.Adam(self.learningRate)
        model.compile(loss="mse", optimizer=opt)

        return model

    def setReward(self, hasEaten, gameEnded):
        self.reward = 0
        if hasEaten:
            self.reward = 10
        if gameEnded:
            self.reward = -10
        return self.reward

    def remember(self, oldState, action, reward, newState, gameEnded):
        self.memory.append((oldState, action, reward, newState, gameEnded))

    def train_short_memory(self, oldState, action, reward, newState, gameEnded):
        targetQ = reward
        if not gameEnded:
            targetQ = reward + self.discount * (np.max(self.model.predict(newState)))
        qValue = self.model.predict(oldState)
        qValue[0][action] = targetQ #Might need to change np.argmax(action) to action
        self.model.fit(oldState, qValue, epochs=1 , verbose=0)

    def replay_memory(self):
        if len(self.memory) > 1000:
            #Select the latest 100 entry in memory, then select rest in random
            firsthalfminibatch = np.flip(self.memory[-100:], 0)
            secondhalfminibatch = random.sample(self.memory[:-100], 900)
            minibatch = np.vstack((firsthalfminibatch, secondhalfminibatch))
        else:
            minibatch = self.memory
        
        for oldState, action, reward, newState, gameEnded in minibatch:
            self.train_short_memory(oldState, action, reward, newState, gameEnded)
