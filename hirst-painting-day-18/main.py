import random
from turtle import Turtle, Screen
# from colorgram import extract
#
# colors = extract('image.jpg', 30)
#
# print(colors)
#
# rgb_colors = []
# for color in colors:
#     color_tuple = (color.rgb.r, color.rgb.g, color.rgb.b)
#     rgb_colors.append(color_tuple)
# print(rgb_colors)

def generate_random_color(turtle):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)
    # turtle.pencolor((r, g, b))
    # turtle.fillcolor((r, g, b))

# for this exercise there is a dot that prints a circle filled
def circle(turtle, radius):
    generate_random_color(turtle)
    timmy.begin_fill()
    timmy.circle(radius)
    timmy.end_fill()

def draw_line_circle(turtle, radius):
    for _ in range(10):
        # circle(timmy, radius)
        timmy.dot(20, generate_random_color(turtle))
        timmy.penup()
        timmy.forward(50)
        timmy.pendown()

def draw_matrix_circles(turtle, radius):
    column_shift = 50
    initial_column = -300
    column = initial_column
    turtle.penup()
    turtle.goto(-300, initial_column)
    for _ in range(10):
        timmy.pendown()
        draw_line_circle(timmy, radius)
        timmy.penup()
        column += column_shift
        timmy.goto(-300, column)

color_list = [(150, 98, 60), (227, 210, 89), (157, 9, 30), (199, 156, 22), (137, 164, 151), (54, 91, 156), (19, 40, 70), (220, 227, 237), (123, 163, 205), (129, 68, 98), (39, 27, 18), (85, 11, 55), (200, 137, 157), (163, 13, 4), (29, 50, 43), (197, 93, 144), (228, 166, 188), (13, 55, 128), (156, 218, 199), (63, 95, 78), (37, 82, 60), (185, 186, 208), (220, 178, 172), (187, 101, 85), (41, 74, 77), (96, 113, 171)]

timmy = Turtle()
timmy.hideturtle()
timmy.speed("fastest")

screen = Screen()
screen.colormode(255)

radius = 10
draw_matrix_circles(timmy, radius)

screen.exitonclick()