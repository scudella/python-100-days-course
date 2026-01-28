from turtle import Turtle

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_shift = +10
        self.y_shift = +10
        self.move_speed = 0.1

    def move(self):
        new_x = self.xcor() + self.x_shift
        new_y = self.ycor() + self.y_shift
        if self.ycor() > 280 or self.ycor() < -280:
            self.y_shift *= -1
            new_y = self.ycor() + self.y_shift
        self.goto(new_x, new_y)

    def bounce_x(self):
        self.x_shift *= -1
        self.move_speed *= 0.9

    def reset_position(self):
        self.goto(0, 0)
        self.x_shift *= -1
        self.move_speed = 0.1
