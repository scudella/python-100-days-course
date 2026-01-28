
from turtle import Turtle, Screen
import random

screen = Screen()
screen.setup(width=500, height=400)
guess = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color: ")
print(guess)

colors = ["red", "orange", "yellow", "green", "blue", "purple"]
y_positions = [-125, -75, -25, 25, 75, 125]
all_turtles = []

for turtle_index in range(0, 6):
    new_turtle = Turtle(shape="turtle")
    new_turtle.penup()
    new_turtle.color(colors[turtle_index])
    new_turtle.goto(x=-230, y=y_positions[turtle_index])
    all_turtles.append(new_turtle)

if guess:
    is_race_on = True

while is_race_on:
    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_race_on = False
            winning_color = turtle.pencolor()
            if winning_color == guess:
                print(f"You won! The {winning_color} turtle wins! ")
            else:
                print(f"You lost! The {winning_color} turtle wins! ")

        turtle.forward(random.randint(0, 10))

# def move_forward():
#     timmy.forward(10)
#
# def move_backward():
#     timmy.backward(10)
#
# def move_counter_clockwise():
#     new_heading = timmy.heading() + 10
#     timmy.setheading(new_heading)
#
# def move_clockwise():
#     new_heading = timmy.heading() - 10
#     timmy.setheading(new_heading)
#
# def clear_drawing():
#     timmy.clear()
#     timmy.penup()
#     timmy.home()
#     timmy.pendown()

screen.listen()
# screen.onkey(key="w", fun=move_forward)
# screen.onkey(key="s", fun=move_backward)
# screen.onkey(key="a", fun=move_counter_clockwise)
# screen.onkey(key="d", fun=move_clockwise)
# screen.onkey(key="c", fun=clear_drawing)
screen.exitonclick()
