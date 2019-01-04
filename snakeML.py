import tkinter
import random
import functools

BLOCK_SIZE = 20
MOVEMENT = 20
BOARD_SIZE = 800


class Snake:
    positionX = 200
    positionY = 200
    speedX = 0
    speedY = 0
    length = 5
    blocksInCanvas = []
    canvas = None

    def __init__(self, canvas):
        self.canvas = canvas

    def moveLeft(self, event):
        self.speedX = -MOVEMENT
        self.speedY = 0

    def moveRight(self, event):
        self.speedX = MOVEMENT
        self.speedY = 0

    def moveUp(self, event):
        self.speedX = 0
        self.speedY = -MOVEMENT

    def moveDown(self, event):
        self.speedX = 0
        self.speedY = MOVEMENT

    def updateMovement(self):
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

    def render(self):
        self.blocksInCanvas.append(canvas.create_rectangle(self.positionX, self.positionY,
                                                           self.positionX+BLOCK_SIZE,
                                                           self.positionY+BLOCK_SIZE,
                                                           fill="white"))
        if self.length < self.blocksInCanvas.__len__():
            toDelete = self.blocksInCanvas.pop(0)
            canvas.delete(toDelete)

    def eat(self, food):
        self.length += 1
        food.eaten()


class Food:
    positionX = 0
    positionY = 0
    canvasId = None
    canvas = None

    def __init__(self, canvas):
        self.canvas = canvas
        first_pass = True
        while snakeCollidedOnFood(snake, self) | first_pass:
            first_pass = False
            self.positionX = random.randint(
                0, BOARD_SIZE/BLOCK_SIZE) * BLOCK_SIZE
            self.positionY = random.randint(
                0, BOARD_SIZE/BLOCK_SIZE) * BLOCK_SIZE

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
        if((food.positionX == blockCoor[0]) & (food.positionY == blockCoor[1])):
            return True
    return False


def gameLoop():
    global snake
    global food
    global canvas
    if snakeCollidedOnFood(snake, food):
        snake.eat(food)
        food = Food(canvas)
        food.render()
    snake.updateMovement()
    snake.render()
    master.after(100, gameLoop)


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

# https://stackoverflow.com/questions/19895877/tkinter-cant-bind-arrow-key-events Try this
