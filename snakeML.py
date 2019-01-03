import tkinter
BLOCK_SIZE = 20
MOVEMENT = 20


master = tkinter.Tk()
canvas = tkinter.Canvas(master, bg="black", height=800, width=800)


class Snake:
    positionX = 200
    positionY = 200
    speedX = 0
    speedY = 0
    length = 2
    rectOnCanvas = []

    def MoveLeft(self, event):
        self.speedX = -MOVEMENT
        self.speedY = 0

    def MoveRight(self, event):
        self.speedX = MOVEMENT
        self.speedY = 0

    def MoveUp(self, event):
        self.speedX = 0
        self.speedY = -MOVEMENT

    def MoveDown(self, event):
        self.speedX = 0
        self.speedY = MOVEMENT


snake = Snake()
def gameLoop():
    snake.positionX += snake.speedX
    snake.positionY += snake.speedY
    snake.rectOnCanvas.append(canvas.create_rectangle(snake.positionX, snake.positionY, 
                              snake.positionX+BLOCK_SIZE,
                              snake.positionY+BLOCK_SIZE, 
                              fill="white"))
    if snake.length < snake.rectOnCanvas.__len__():
        toDelete = snake.rectOnCanvas.pop(0)
        canvas.delete(toDelete)
    print("{0}:{1}\n".format(snake.positionX, snake.positionY))
    print("{0}:{1}".format(snake.speedX, snake.speedY))
    master.after(200, gameLoop)


master.bind('<Left>', snake.MoveLeft)
master.bind('<Right>', snake.MoveRight)
master.bind('<Up>', snake.MoveUp)
master.bind('<Down>', snake.MoveDown)
snake.rectOnCanvas.append(canvas.create_rectangle(snake.positionX, snake.positionY, 
                        snake.positionX+BLOCK_SIZE, snake.positionY+BLOCK_SIZE, 
                        fill="white"))
master.after(1000, gameLoop)
canvas.grid()
master.mainloop()
