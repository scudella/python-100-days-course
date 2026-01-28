from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10

class Car(Turtle):
    def __init__(self):
        super().__init__()
        self.color(random.choice(COLORS))
        self.penup()
        self.setheading(180)
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=2)


class CarManager:
    def __init__(self):
        super().__init__()
        self.cars = []
        self.spawn_cars(15)
        self.car_speed = 0.1

    def spawn_cars(self, amount):
        for _ in range(amount):
            car = Car()
            x_coord = random.randrange(-260, 260, 50)
            y_coord = random.randrange(-240, 260, 40)
            car.goto(x_coord, y_coord)
            self.cars.append(car)

    def move_cars(self):
        for car in self.cars:
            car.forward(MOVE_INCREMENT)
            if car.xcor() < -280:
                car.goto(260, car.ycor())

    def increase_speed(self):
        self.car_speed *= 0.9