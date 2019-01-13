import snakeML
from DeepQNetwork import DeepQNetworkAgent
import numpy as np

score_plot = []
counter_plot = []

def gameInit(agentDQN, displayUI=False):
    snakeML.newGameML()
    snakeML.startGameML(showGui=displayUI)
    state_1 = np.reshape(snakeML.getInputLayer(), (1, 16))
    action = 1
    foodAte, gameEnded = snakeML.nextStep(1)
    state_2 = np.reshape(snakeML.getInputLayer(), (1, 16))
    reward = agentDQN.setReward(foodAte, gameEnded)
    agentDQN.remember(state_1, action, reward, state_2, gameEnded)
    agentDQN.replay_memory()


def run():
    agentDQN = DeepQNetworkAgent()
    current_episode = 0
    max_episode = 150
    for current_episode in range(max_episode):
        gameInit(agentDQN, displayUI=False) #change boolean to display UI
        agentDQN.explorationEpsilon -= agentDQN.epsilonDecay
        if agentDQN.explorationEpsilon < 0.1:
            agentDQN.explorationEpsilon = 0.1
        while not snakeML.gameEnded:
            state_1 = np.reshape(snakeML.getInputLayer(), (1, 16))
            if np.random.random_sample() < agentDQN.explorationEpsilon:
                action = np.random.randint(0, 3)
            else:
                prediction = agentDQN.model.predict(np.reshape(state_1, (1, 16)))
                action = np.argmax(prediction)
            foodAte, gameEnded = snakeML.nextStep(action)
            reward = agentDQN.setReward(foodAte, gameEnded)
            state_2 = np.reshape(snakeML.getInputLayer(), (1, 16))
            agentDQN.remember(state_1, action, reward, state_2, gameEnded)
            agentDQN.train_short_memory(state_1, action, reward, state_2, gameEnded)
            result = snakeML.getSnakeLength()
        agentDQN.replay_memory()
        print(f"Game {current_episode}, Score={snakeML.getSnakeLength()}")
        score_plot.append(snakeML.getSnakeLength())
        counter_plot.append(current_episode)
        snakeML.exit()
    agentDQN.model.save("model/weights.hdf5")
    
            
            
run()

    


