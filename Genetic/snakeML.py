import time
import tkinter
import random
import functools
import numpy as np

BLOCK_SIZE = 20
MOVEMENT = 20
BOARD_SIZE = 400
SNAKE_BODY_TAG = "0"
FOOD_TAG = "1"


class Snake:
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3
    NO_DIRECTION = -1

    def __init__(self, canvas):
        self.canvas = canvas
        self.position = [100, 100]  # x,y coor
        self.speedX = MOVEMENT
        self.speedY = 0
        self.length = 1
        self.blocksInCanvas = []
        self.currentDirection = self.RIGHT
        self.directionInput = self.NO_DIRECTION
        self.headBlockCanvasID = canvas.create_rectangle(
            self.position[0], self.position[1], self.position[0] + BLOCK_SIZE-1, self.position[1] + BLOCK_SIZE-1, fill="green")

    def move(self, direction):
        if direction == self.LEFT:
            self.moveLeft(None)
        elif direction == self.UP:
            self.moveUp(None)
        elif direction == self.RIGHT:
            self.moveRight(None)
        elif direction == self.DOWN:
            self.moveDown(None)

    def moveLeft(self, event):
        if not self.isMovingInOppositeDirection(self.LEFT):
            self.directionInput = self.LEFT
            self.speedX = -MOVEMENT
            self.speedY = 0

    def moveRight(self, event):
        if not self.isMovingInOppositeDirection(self.RIGHT):
            self.directionInput = self.RIGHT
            self.speedX = MOVEMENT
            self.speedY = 0

    def moveUp(self, event):
        if not self.isMovingInOppositeDirection(self.UP):
            self.directionInput = self.UP
            self.speedX = 0
            self.speedY = -MOVEMENT

    def moveDown(self, event):
        if not self.isMovingInOppositeDirection(self.DOWN):
            self.directionInput = self.DOWN
            self.speedX = 0
            self.speedY = MOVEMENT

    def updateMovement(self):
        # 0 = no direction
        if(self.directionInput != self.NO_DIRECTION):
            self.currentDirection = self.directionInput
        self.directionInput = self.NO_DIRECTION
        self.position[0] += snake.speedX
        self.position[1] += snake.speedY

    def isMovingInOppositeDirection(self, newDirection):
        # Commented to teach snakes.
        # if((newDirection + 2) % 4 == self.currentDirection):
        #    return True
        # return False
        return False

    def render(self):
        self.blocksInCanvas.append(canvas.create_rectangle(self.position[0], self.position[1],
                                                           self.position[0] +
                                                           BLOCK_SIZE-1,
                                                           self.position[1] +
                                                           BLOCK_SIZE-1,
                                                           fill="white",
                                                           tags=SNAKE_BODY_TAG))
        canvas.coords(self.headBlockCanvasID, self.position[0], self.position[1],
                      self.position[0] +
                      BLOCK_SIZE-1,
                      self.position[1] +
                      BLOCK_SIZE-1)
        canvas.tag_raise(self.headBlockCanvasID)
        if self.length < len(self.blocksInCanvas):
            toDelete = self.blocksInCanvas.pop(0)
            canvas.delete(toDelete)

    def eat(self, food):
        self.length += 1
        food.eaten()


class Food:

    def __init__(self, canvas):
        global snake
        self.position = [140, 140]
        self.canvas = canvas
        #first_pass = True
        while snakeCollidedOnFood(snake, self):  # | first_pass:
            first_pass = False
            self.position[0] = random.randint(
                0, (BOARD_SIZE/BLOCK_SIZE) - 1) * BLOCK_SIZE
            self.position[1] = random.randint(
                0, (BOARD_SIZE/BLOCK_SIZE) - 1) * BLOCK_SIZE

    def render(self):
        self.canvasId = canvas.create_rectangle(self.position[0], self.position[1],
                                                self.position[0] +
                                                BLOCK_SIZE-1,
                                                self.position[1] +
                                                BLOCK_SIZE-1,
                                                fill="red",
                                                tags=FOOD_TAG)

    def eaten(self):
        canvas.delete(self.canvasId)
        self = None


def snakeCollidedOnFood(snake, food):
    for block in snake.blocksInCanvas:
        blockCoor = canvas.coords(block)
        # blockCoor is a tuple(x1,y1,x2,y2)
        if(isCollided(food.position[0], food.position[1], blockCoor[0], blockCoor[1])):
            return True
    return False


def snakeCollidedOnWall(snake):
    if(snake.position[0] >= BOARD_SIZE or snake.position[0] < 0 or snake.position[1] >= BOARD_SIZE or snake.position[1] < 0):
        return True
    return False


def snakeCollidedOnTail(snake):
    headBlock = snake.blocksInCanvas[-1]
    headBlockCoor = canvas.coords(headBlock)
    for i in range(0, len(snake.blocksInCanvas)-1):
        block = snake.blocksInCanvas[i]
        blockCoor = canvas.coords(block)
        if (isCollided(headBlockCoor[0], headBlockCoor[1], blockCoor[0], blockCoor[1])):
            return True
    return False


def isCollided(x1, y1, x2, y2):
    if((x1 == x2) & (y1 == y2)):
        return True
    return False


def resetBoard():
    global food
    global snake
    global canvas
    canvas.delete("all")
    snake = Snake(canvas)
    snake.render()
    food = Food(canvas)
    food.render()
    master.bind('<Left>', snake.moveLeft)
    master.bind('<Right>', snake.moveRight)
    master.bind('<Up>', snake.moveUp)
    master.bind('<Down>', snake.moveDown)


def gameLoop():
    global snake
    global food
    global canvas
    if snakeCollidedOnFood(snake, food):
        snake.eat(food)
        food = Food(canvas)
        food.render()
    if snakeCollidedOnTail(snake):
        resetBoard()
    if snakeCollidedOnWall(snake):
        resetBoard()
    snake.updateMovement()
    snake.render()
    master.after(100, gameLoop)


def startGame():
    master.after(100, gameLoop)
    canvas.grid()
    master.mainloop()


def newGame():
    global snake
    global food
    global canvas
    global master
    global canvas

    master = tkinter.Tk()
    canvas = tkinter.Canvas(
        master, bg="black", height=BOARD_SIZE, width=BOARD_SIZE)
    snake = Snake(canvas)
    food = Food(canvas)
    snake.render()
    food.render()
    master.bind('<Left>', snake.moveLeft)
    master.bind('<Right>', snake.moveRight)
    master.bind('<Up>', snake.moveUp)
    master.bind('<Down>', snake.moveDown)


if __name__ == '__main__':
    newGame()
    startGame()


#################### The following code are used for machine learning for the snake AI ###############################################

# Turn snake to the left of its current direction
def snakeMoveLeft(object):
    direction = (snake.currentDirection + 1) % 4
    snake.move(direction)


def snakeMoveFront(object):
    direction = (snake.currentDirection)
    snake.move(direction)

# Turn snake to the right of its current direction


def snakeMoveRight(object):
    direction = (snake.currentDirection - 1) % 4
    snake.move(direction)


def nextStep(actionToDo):
    global snake
    global foodAte
    foodAte = False
    actions[actionToDo](snake)
    gameLoopML()
    return foodAte, gameEnded

# Allow an instance of game to be started that is not governed by tkinter mainloop/after methods


def startGameML(showGui=True):
    global displaySnakeCanvas
    displaySnakeCanvas = showGui
    if not displaySnakeCanvas:
        master.withdraw()
    canvas.grid()
    gameLoopML()


# Allow an instance of game to be started that is not governed by tkinter mainloop/after methods
def newGameML():
    global actions
    global gameEnded
    global snake
    global food
    global canvas
    global master
    global canvas
    global score

    score = 0
    gameEnded = False
    master = tkinter.Tk()
    canvas = tkinter.Canvas(
        master, bg="black", height=BOARD_SIZE, width=BOARD_SIZE)
    snake = Snake(canvas)
    food = Food(canvas)
    snake.render()
    food.render()
    actions = [snakeMoveLeft, snakeMoveFront, snakeMoveRight]


def gameLoopML():
    global snake
    global food
    global canvas
    global score
    global gameEnded
    global foodAte
    snake.updateMovement()
    snake.render()
    if snakeCollidedOnFood(snake, food):
        foodAte = True
        score += 1
        snake.eat(food)
        food = Food(canvas)
        food.render()
    if snakeCollidedOnTail(snake):
        gameEnded = True
        score -= 20
    if snakeCollidedOnWall(snake):
        gameEnded = True
        score -= 20
    updateInputLayer()
    master.update()
    global displaySnakeCanvas
    if displaySnakeCanvas:
        time.sleep(0.05)


def exit():
    master.destroy()


def lookInDirection(snake, vectorX, vectorY):
    global canvas
    # 0 -> tail 1 -> wall
    itemsInDirection = np.zeros(2)
    distance = 0
    currentPosition = snake.position
    currentPosition += np.asarray([vectorX, vectorY])
    distance += 1
    tailFound = False
    while not(currentPosition[0] >= BOARD_SIZE or currentPosition[0] < 0 or currentPosition[1] >= BOARD_SIZE or currentPosition[1] < 0):
        itemsInCurrentPosition = canvas.find_overlapping(
            currentPosition[0], currentPosition[1], currentPosition[0]+BLOCK_SIZE-1, currentPosition[1]+BLOCK_SIZE-1)
        for item in itemsInCurrentPosition:
            tag = canvas.gettags(item)[0]
            if not tailFound and tag == SNAKE_BODY_TAG:
                itemsInDirection[0] = 1 / distance
                tailFound = True
        currentPosition += np.asarray([vectorX, vectorY])
        distance += 1
    itemsInDirection[1] = 1 / distance
    return itemsInDirection


def updateInputLayer():
    global inputLayer
    global snake
    inputLayer = np.zeros(14)

    snakeMoveLeft(None)
    itemInDirection = lookInDirection(snake, snake.speedX, snake.speedY)
    inputLayer[0] = itemInDirection[0]
    inputLayer[1] = itemInDirection[1]

    snakeMoveFront(None)
    itemInDirection = lookInDirection(snake, snake.speedX, snake.speedY)
    inputLayer[2] = itemInDirection[0]
    inputLayer[3] = itemInDirection[1]

    snakeMoveRight(None)
    itemInDirection = lookInDirection(snake, snake.speedX, snake.speedY)
    inputLayer[4] = itemInDirection[0]
    inputLayer[5] = itemInDirection[1]
    # Reset back direction of snake
    snakeMoveFront(None)

    snakeDirection = [0, 0, 0, 0]
    if(snake.currentDirection == snake.LEFT):
        snakeDirection[0] = 1
    elif(snake.currentDirection == snake.RIGHT):
        snakeDirection[1] = 1
    elif(snake.currentDirection == snake.UP):
        snakeDirection[2] = 1
    elif(snake.currentDirection == snake.DOWN):
        snakeDirection[3] = 1

    inputLayer[6] = snakeDirection[0]
    inputLayer[7] = snakeDirection[1]
    inputLayer[8] = snakeDirection[2]
    inputLayer[9] = snakeDirection[3]

    # if food.position[0] < snake.position[0]:
    #     inputLayer[10] = 1 / ((snake.position[0] - food.position[0]) / BLOCK_SIZE)
    # if food.position[0] > snake.position[0]:
    #     inputLayer[11] = 1 / ((food.position[0] - snake.position[0]) / BLOCK_SIZE)
    # if food.position[1] < snake.position[1]:
    #     inputLayer[12] = 1 / ((snake.position[1] - food.position[1]) / BLOCK_SIZE)
    # if food.position[1] > snake.position[1]:
    #     inputLayer[13] = 1 / ((food.position[1] - snake.position[1]) / BLOCK_SIZE)

    inputLayer[10] = food.position[0] < snake.position[0]
    inputLayer[11] = food.position[0] > snake.position[0]
    inputLayer[12] = food.position[1] < snake.position[1]
    inputLayer[13] = food.position[1] > snake.position[1]


def getInputLayer():
    global inputLayer
    return inputLayer


def isNextDirectionBlocked(snake):
    nextBlockPosition = snake.position + \
        np.asarray([snake.speedX, snake.speedY])
    for block in snake.blocksInCanvas:
        blockCoor = canvas.coords(block)
        if (isCollided(nextBlockPosition[0], nextBlockPosition[1], blockCoor[0], blockCoor[1])):
            return True
    return False


def getSnakeLength():
    global snake
    return snake.length
