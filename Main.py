from turtle import Turtle, Screen
from random import randint, choice
import time

# Thiết lập màn hình
display = Screen()
display.setup(500, 600)
display.bgcolor("black")
display.tracer(0)


display.addshape("car.gif")

class Player(Turtle):  
    def __init__(self):  
        super().__init__()  
        self.shape("car.gif") 
        self.penup()
        self.goto(0, -250)  
        self.speed = 10
        self.direction = "stop" 

    def move(self):
        if self.direction == "up":
            self.goto(self.xcor(), self.ycor() + self.speed)
        elif self.direction == "down":
            self.goto(self.xcor(), self.ycor() - self.speed)
        elif self.direction == "left":
            self.goto(self.xcor() - self.speed, self.ycor())
        elif self.direction == "right":
            self.goto(self.xcor() + self.speed, self.ycor())

        display.ontimer(self.move, 50)

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

class Vehicle:
    def __init__(self):
        self.list_car = []

    def create_car(self):
        if randint(1, 8) == 5:
            carr = Turtle()
            carr.shape("car.gif")  
            carr.penup()
            toado_y = randint(-220, 220)
            carr.goto(200, toado_y)
            self.list_car.append(carr)

    def move_cars(self):
        for x in self.list_car:
            x.backward(3)

player = Player()
xe = Vehicle()

display.listen()
display.onkey(player.move_up, "Up")
display.onkey(player.move_down, "Down")
display.onkey(player.move_left, "Left")
display.onkey(player.move_right, "Right")

player.move()

# Vòng lặp chính
running = True
while running:
    time.sleep(0.1)
    display.update()
    xe.create_car()
    xe.move_cars()

display.exitonclick()
