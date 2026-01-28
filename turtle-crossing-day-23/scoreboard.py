from turtle import Turtle

FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.penup()
        self.hideturtle()
        self.score_update()

    def score_update(self):
        self.clear()
        self.goto(-220,220)
        self.write(f"Level {self.level}", align="center", font=FONT)

    def game_over(self):
        self.goto(-30, 0)
        self.write("game over", align="center", font=FONT)

    def increase_score(self):
        self.level += 1
        self.score_update()