from turtle import Turtle, Screen
import random

def draw_square(turtle, size, color):
    turtle.color(color)
    for _ in range(4):
        turtle.right(90)
        turtle.forward(size)

def draw_polygon(turtle, size, sides):
    angle = 360 / sides
    for _ in range(sides):
        turtle.right(angle)
        turtle.forward(size)

def draw_dashed_line(turtle, size, length):
    for _ in range(length):
        turtle.pendown()
        turtle.forward(size)
        turtle.penup()
        turtle.forward(size)

def draw_triangle_up_to_decagon(turtle, size):
    for sides in range(3, 11):
        generate_random_color(turtle)
        draw_polygon(turtle, size, sides)

def generate_random_color(turtle):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    turtle.pencolor((r, g, b))

def random_walk(turtle, path):
    turtle.pensize(10)
    turtle.speed(5)
    for _ in range(path):
        turtle.setheading(random.choice([0, 90, 180, 270]))
        generate_random_color(turtle)
        turtle.forward(20)

def spirograph(turtle, radius, angle_turn):
    turtle.speed(7)
    for _ in range(360 // angle_turn):
        generate_random_color(turtle)
        timmy.circle(radius)
        timmy.right(angle_turn)


timmy = Turtle()
timmy.shape("turtle")
# timmy.color("green4")

# draw_square(timmy, 100, "red")
# draw_dashed_line(timmy, 10, 15, "green4")
screen = Screen()
screen.colormode(255)

angle_turn = 5
radius = 100
spirograph(timmy, radius, angle_turn)

# draw_triangle_up_to_decagon(timmy, 100)
# random_walk(timmy, 300)

screen.exitonclick()