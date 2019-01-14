import keras
import snakeML
import numpy as np

weightsToUse = "model/weights200.hdf5"
model = keras.Sequential()
model.add(keras.layers.Dense(120, activation="relu", input_dim=11))
model.add(keras.layers.Dropout(0.15))
model.add(keras.layers.Dense(120, activation="relu"))
model.add(keras.layers.Dropout(0.15))
model.add(keras.layers.Dense(120, activation="relu"))
model.add(keras.layers.Dropout(0.15))
model.add(keras.layers.Dense(3, activation="softmax"))
opt = keras.optimizers.Adam(0.0001)
model.compile(loss="mse", optimizer=opt)

model.load_weights(weightsToUse)

while True:
    snakeML.newGameML()
    snakeML.startGameML(showGui=True)
    while not snakeML.gameEnded:
        state = np.reshape(snakeML.getInputLayer(), (1,11))
        output = model.predict(state)
        action = np.argmax(output)
        snakeML.nextStep(action)
    snakeML.exit()