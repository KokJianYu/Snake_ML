import snakeML
from DeepQNetwork import DeepQNetworkAgent
import numpy as np

SIZE_INPUT_LAYER = 14

def gameInit(agentDQN, displayUI=False):
    snakeML.newGameML()
    snakeML.startGameML(showGui=displayUI)
    state_1 = np.reshape(snakeML.getInputLayer(), (1, SIZE_INPUT_LAYER))
    action = 1
    foodAte, gameEnded = snakeML.nextStep(1)
    state_2 = np.reshape(snakeML.getInputLayer(), (1, SIZE_INPUT_LAYER))
    reward = agentDQN.setReward(foodAte, gameEnded)
    agentDQN.remember(state_1, action, reward, state_2, gameEnded)
    agentDQN.replay_memory()


def run():
    agentDQN = DeepQNetworkAgent()
    current_episode = 0
    max_episode = 401
    for current_episode in range(max_episode):
        gameInit(agentDQN, displayUI=False) #change boolean to display UI
        #Decrease exploration epsilon after every episode
        agentDQN.explorationEpsilonDecay()
        while not snakeML.gameEnded:
            
            state_1 = np.reshape(snakeML.getInputLayer(), (1, SIZE_INPUT_LAYER))
            if np.random.random_sample() < agentDQN.explorationEpsilon:
                action = np.random.randint(0, 3)
            else:
                prediction = agentDQN.model.predict(np.reshape(state_1, (1, SIZE_INPUT_LAYER)))
                action = np.argmax(prediction)
            foodAte, gameEnded = snakeML.nextStep(action)
            reward = agentDQN.setReward(foodAte, gameEnded)
            state_2 = np.reshape(snakeML.getInputLayer(), (1, SIZE_INPUT_LAYER))
            agentDQN.train_short_memory(state_1, action, reward, state_2, gameEnded)
            agentDQN.remember(state_1, action, reward, state_2, gameEnded)
        agentDQN.replay_memory()
        print(f"Game {current_episode}, Score={snakeML.getSnakeLength()-1}")
        snakeML.exit()
        if((current_episode % 10)==0):
            agentDQN.model.save(f"model/episode_{current_episode:03d}.hdf5")
    
            
            
run()

    


