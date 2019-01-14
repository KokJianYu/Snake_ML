import snakeML
from DeepQNetwork import DeepQNetworkAgent
import numpy as np
from DQN import DQNAgent

score_plot = []
counter_plot = []

def gameInit(agentDQN, displayUI=False):
    snakeML.newGameML()
    snakeML.startGameML(showGui=displayUI)
    state_1 = np.reshape(snakeML.getInputLayer(), (1, 11))
    action = 1
    foodAte, gameEnded = snakeML.nextStep(1)
    state_2 = np.reshape(snakeML.getInputLayer(), (1, 11))
    reward = agentDQN.setReward(foodAte, gameEnded)
    agentDQN.remember(state_1, action, reward, state_2, gameEnded)
    agentDQN.replay_memory()


def run():
    agentDQN = DeepQNetworkAgent()
    current_episode = 0
    max_episode = 1000
    for current_episode in range(max_episode):
        gameInit(agentDQN, displayUI=False) #change boolean to display UI
        agentDQN.explorationEpsilon = agentDQN.explorationEpsilon - agentDQN.epsilonDecay
        if agentDQN.explorationEpsilon < 0.05:
            agentDQN.explorationEpsilon = 0.05
        while not snakeML.gameEnded:
            
            state_1 = np.reshape(snakeML.getInputLayer(), (1, 11))
            if np.random.random_sample() < agentDQN.explorationEpsilon:
                action = np.random.randint(0, 3)
            else:
                prediction = agentDQN.model.predict(np.reshape(state_1, (1, 11)))
                action = np.argmax(prediction)
            foodAte, gameEnded = snakeML.nextStep(action)
            reward = agentDQN.setReward(foodAte, gameEnded)
            state_2 = np.reshape(snakeML.getInputLayer(), (1, 11))
            agentDQN.train_short_memory(state_1, action, reward, state_2, gameEnded)
            agentDQN.remember(state_1, action, reward, state_2, gameEnded)
        agentDQN.replay_memory()
        print(f"Game {current_episode}, Score={snakeML.getSnakeLength()-1}")
        score_plot.append(snakeML.getSnakeLength())
        counter_plot.append(current_episode)
        snakeML.exit()
        if((current_episode % 50)==0):
            agentDQN.model.save(f"model/weights{current_episode}.hdf5")
    
            
            
run()

    


