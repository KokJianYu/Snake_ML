import keras
import numpy as np
import pandas as pd
import random

class DeepQNetworkAgent(object):

    def __init__(self):
        self.learningRate = 0.0005
        self.model = self.createModel()
        self.explorationEpsilon = 0.96
        self.epsilonDecay = 0.01
        self.memory = [] #Used to store [oldState, action, reward, newState, gameEnded]
        self.reward = 0
        self.discount = 0.9


    def createModel(self, weights=None):
        model = keras.Sequential()
        model.add(keras.layers.Dense(120, activation="relu", input_dim=16))
        model.add(keras.layers.Dense(120, activation="relu"))
        model.add(keras.layers.Dense(3, activation="softmax"))
        opt = keras.optimizers.Adam(self.learningRate)
        model.compile(loss="mse", optimizer=opt)

        if weights:
            model.set_weights(weights)

        return model

    def setReward(self, hasEaten, isDead):
        self.reward = 0
        if hasEaten:
            self.reward = 10
        if isDead:
            self.reward = -10
        return self.reward

    def remember(self, oldState, action, reward, newState, gameEnded):
        self.memory.append((oldState, action, reward, newState, gameEnded))

    def train_short_memory(self, oldState, action, reward, newState, gameEnded):
        targetQ = reward
        if not gameEnded:
            targetQ = reward + self.discount * (np.max(self.model.predict(newState)))
        qValue = self.model.predict(oldState)
        qValue[np.argmax(action)] = targetQ #Might need to change np.argmax(action) to action
        self.model.fit(oldState, qValue, epochs=1 , verbose=0)

    def replay_memory(self):
        if len(self.memory) > 1000:
            minibatch = random.sample(self.memory, 1000)
        else:
            minibatch = self.memory
        
        for oldState, action, reward, newState, gameEnded in minibatch:
            self.train_short_memory(oldState, action, reward, newState, gameEnded)
