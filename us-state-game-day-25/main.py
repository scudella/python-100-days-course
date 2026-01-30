from turtle import Screen, Turtle
import pandas

screen = Screen()
screen.setup(width=750, height=500)
screen.title("U. S. States Game")

image = "blank_states_img.gif"
screen.addshape(image)


timmy = Turtle()
timmy.speed(0)
timmy.shape(image)

data = pandas.read_csv("50_states.csv")

all_states = []

while len(all_states) < 50:
    answer_state = screen.textinput(title=f"{len(all_states)}/50 States Correct", prompt="What's another state's name?").title()
    state_row = data[data['state'] == answer_state]

    if answer_state == "Exit":
        break

    if len(state_row.state) != 0:
        my_turtle = Turtle()
        my_turtle.penup()
        my_turtle.hideturtle()
        my_turtle.goto((state_row['x'].item(), state_row['y'].item()))
        my_turtle.write(answer_state, align="center", font=("Courier", 10, "normal"))
        all_states.append(answer_state)



all_states_list = data.state.to_list()

missing_states = []
for state in all_states_list:
    if state not in all_states:
        missing_states.append(state)

state_dict = {
    "state name": missing_states
}

# pandas.DataFrame(state_dict).to_csv("all_states.csv", index=False)
pandas.DataFrame(state_dict).to_csv("missing_states.csv")

screen.exitonclick()
