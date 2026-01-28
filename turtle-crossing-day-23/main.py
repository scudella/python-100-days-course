import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(player.up, "Up")




game_is_on = True
while game_is_on:
    time.sleep(car_manager.car_speed)
    screen.update()
    if player.ycor() > 280:
        player.start_position()
        scoreboard.increase_score()
        car_manager.increase_speed()
    car_manager.move_cars()

    for car in car_manager.cars:
        if player.distance(car) < 20:
            game_is_on = False
            break

scoreboard.game_over()
screen.exitonclick()
