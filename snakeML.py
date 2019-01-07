import tkinter
import random
import functools

BLOCK_SIZE = 20
MOVEMENT = 20
BOARD_SIZE = 800


class Snake:
    LEFT = -1
    RIGHT = 1
    UP = -2
    DOWN = 2
    def __init__(self, canvas):
        self.canvas = canvas
        self.positionX = 200
        self.positionY = 200
        self.speedX = MOVEMENT
        self.speedY = 0
        self.length = 5
        self.blocksInCanvas = []
        self.canvas = None
        self.currentDirection = self.RIGHT
        self.directionInput = 0

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
        if(self.directionInput != 0): 
            self.currentDirection = self.directionInput
        self.directionInput = 0
        self.positionX += snake.speedX
        self.positionY += snake.speedY
        if(self.positionX >= BOARD_SIZE):
            self.positionX -= BOARD_SIZE
        elif(self.positionX < 0):
            self.positionX += BOARD_SIZE
        if(self.positionY >= BOARD_SIZE):
            self.positionY -= BOARD_SIZE
        elif(self.positionY < 0):
            self.positionY += BOARD_SIZE

    def isMovingInOppositeDirection(self, newDirection):
        if(newDirection * -1 == self.currentDirection):
            return True
        return False

    def render(self):
        self.blocksInCanvas.append(canvas.create_rectangle(self.positionX, self.positionY,
                                                           self.positionX+BLOCK_SIZE,
                                                           self.positionY+BLOCK_SIZE,
                                                           fill="white"))
        if self.length < len(self.blocksInCanvas):
            toDelete = self.blocksInCanvas.pop(0)
            canvas.delete(toDelete)

    def eat(self, food):
        self.length += 1
        food.eaten()


class Food:
    canvasId = None
    canvas = None

    def __init__(self, canvas):
        global snake
        self.positionX = 0
        self.positionY = 0
        self.canvas = canvas
        first_pass = True
        while snakeCollidedOnFood(snake, self) | first_pass:
            first_pass = False
            self.positionX = random.randint(
                0, (BOARD_SIZE/BLOCK_SIZE) - 1) * BLOCK_SIZE
            self.positionY = random.randint(
                0, (BOARD_SIZE/BLOCK_SIZE) - 1) * BLOCK_SIZE

    def render(self):
        self.canvasId = canvas.create_rectangle(self.positionX, self.positionY,
                                                self.positionX+BLOCK_SIZE,
                                                self.positionY+BLOCK_SIZE,
                                                fill="red")

    def eaten(self):
        canvas.delete(self.canvasId)
        self = None


def snakeCollidedOnFood(snake, food):
    for block in snake.blocksInCanvas:
        blockCoor = canvas.coords(block)
        # blockCoor is a tuple(x1,y1,x2,y2)
        if(isCollided(food.positionX, food.positionY, blockCoor[0], blockCoor[1])):
            return True
    return False

def snakeCollidedOnTail(snake):
    headBlock = snake.blocksInCanvas[-1]
    headBlockCoor = canvas.coords(headBlock)
    for i in range(0,len(snake.blocksInCanvas)-1):
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
    snake.updateMovement()
    snake.render()
    master.after(100, gameLoop)

global snake
global food
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
master.after(100, gameLoop)
canvas.grid()
master.mainloop()

