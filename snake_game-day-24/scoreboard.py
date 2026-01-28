from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = int(self.get_high_score())
        self.penup()
        self.color("white")
        self.hideturtle()
        self.goto(x=0, y=270)
        self.update_scoreboard()

    def get_high_score(self):
        with open("data.txt", "r") as file:
            return file.read()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", align="center", font=("Courier", 16, "bold"))

    def increase_score(self):
        self.score += 1
        self.update_scoreboard()

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            file = open("data.txt", "w")
            file.write(str(self.high_score))
            file.close()
        self.score = 0
        self.update_scoreboard()