import random
import time
import turtle

# --- Screen Setup ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = turtle.Screen()
screen.title("Breakout")
screen.bgcolor("#111111")
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.tracer(0)  # Turn off auto-updates for smooth manual animation

# --- Game State Variables ---
score = 0
lives = 3
game_over = False
game_paused = False

# --- UI / Scoreboard ---
hud = turtle.Turtle()
hud.speed(0)
hud.color("white")
hud.penup()
hud.hideturtle()
hud.goto(0, 260)


def update_hud():
    hud.clear()
    hud.write(
        f"SCORE: {score}    LIVES: {lives}",
        align="center",
        font=("Courier", 20, "bold"),
    )


# --- Paddle ---
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("#00FFFF")
paddle.shapesize(stretch_wid=1, stretch_len=6)  # 20px tall, 120px wide
paddle.penup()
paddle.goto(0, -250)

PADDLE_SPEED = 35
PADDLE_HALF_WIDTH = 60

# --- Ball ---
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("#FFFFFF")
ball.penup()
ball.goto(0, -220)

BASE_SPEED = 4.5
ball.dx = random.choice([-BASE_SPEED, BASE_SPEED])
ball.dy = BASE_SPEED
BALL_RADIUS = 10

# --- Bricks Setup ---
bricks = []
ROWS = 5
COLS = 10
BRICK_WIDTH = 70  # stretch_len = 3.5 (20 * 3.5)
BRICK_HEIGHT = 20  # stretch_wid = 1.0 (20 * 1.0)
X_GAP = 6
Y_GAP = 8
START_X = -342
START_Y = 210

# Breakout row colors and point values
ROW_CONFIG = [
    ("#FF3B30", 7),  # Red
    ("#FF9500", 7),  # Orange
    ("#FFCC00", 4),  # Yellow
    ("#34C759", 4),  # Green
    ("#007AFF", 1),  # Blue
]


def create_bricks():
    for b in bricks:
        b.hideturtle()
    bricks.clear()

    for row in range(ROWS):
        color, points = ROW_CONFIG[row]
        for col in range(COLS):
            brick = turtle.Turtle()
            brick.speed(0)
            brick.shape("square")
            brick.color(color)
            brick.shapesize(stretch_wid=1, stretch_len=3.5)
            brick.penup()

            x = START_X + col * (BRICK_WIDTH + X_GAP)
            y = START_Y - row * (BRICK_HEIGHT + Y_GAP)
            brick.goto(x, y)
            brick.points = points  # Attach custom attribute for scoring
            bricks.append(brick)


# --- Controls ---

keys_pressed = {"left": False, "right": False}
PADDLE_SPEED = 7  # Adjusted for per-frame movement (instead of per-keypress)


def press_left():
    keys_pressed["left"] = True


def release_left():
    keys_pressed["left"] = False


def press_right():
    keys_pressed["right"] = True


def release_right():
    keys_pressed["right"] = False


def update_paddle():
    if game_over or game_paused:
        return

    new_x = paddle.xcor()
    if keys_pressed["left"]:
        new_x -= PADDLE_SPEED
    if keys_pressed["right"]:
        new_x += PADDLE_SPEED

    # Keep paddle inside screen boundaries
    left_limit = -SCREEN_WIDTH // 2 + PADDLE_HALF_WIDTH + 10
    right_limit = SCREEN_WIDTH // 2 - PADDLE_HALF_WIDTH - 10
    new_x = max(left_limit, min(right_limit, new_x))

    paddle.setx(new_x)

def reset_ball():
    ball.goto(0, -220)
    paddle.goto(0, -250)
    ball.dx = random.choice([-BASE_SPEED, BASE_SPEED])
    ball.dy = BASE_SPEED

def restart_game():
    global score, lives, game_over
    if game_over:
        score = 0
        lives = 3
        game_over = False
        msg_turtle.clear()
        create_bricks()
        reset_ball()
        update_hud()

# Message turtle for Game Over / Win text
msg_turtle = turtle.Turtle()
msg_turtle.speed(0)
msg_turtle.color("white")
msg_turtle.penup()
msg_turtle.hideturtle()

# Keyboard Bindings (Press + Release)
screen.listen()
screen.onkeypress(press_left, "Left")
screen.onkeyrelease(release_left, "Left")
screen.onkeypress(press_right, "Right")
screen.onkeyrelease(release_right, "Right")

screen.onkeypress(press_left, "a")
screen.onkeyrelease(release_left, "a")
screen.onkeypress(press_right, "d")
screen.onkeyrelease(release_right, "d")

screen.onkeypress(restart_game, "r")
screen.onkeypress(restart_game, "R")

# --- Initialize Game ---
create_bricks()
update_hud()

# --- Main Game Loop ---
while True:
    screen.update()
    time.sleep(0.01)  # ~100 FPS cap for consistent speed across machines

    if game_over:
        continue

    update_paddle()  # Moves smoothly at 100 FPS with zero OS repeat delay

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # 1. Wall Collisions (Left & Right)
    if ball.xcor() + BALL_RADIUS > SCREEN_WIDTH // 2:
        ball.setx(SCREEN_WIDTH // 2 - BALL_RADIUS)
        ball.dx *= -1

    if ball.xcor() - BALL_RADIUS < -SCREEN_WIDTH // 2:
        ball.setx(-SCREEN_WIDTH // 2 + BALL_RADIUS)
        ball.dx *= -1

    # 2. Ceiling Collision
    if ball.ycor() + BALL_RADIUS > SCREEN_HEIGHT // 2:
        ball.sety(SCREEN_HEIGHT // 2 - BALL_RADIUS)
        ball.dy *= -1

    # 3. Bottom Floor Collision (Lose a life)
    if ball.ycor() - BALL_RADIUS < -SCREEN_HEIGHT // 2:
        lives -= 1
        update_hud()
        if lives <= 0:
            game_over = True
            msg_turtle.goto(0, 0)
            msg_turtle.write(
                "GAME OVER\nPress 'R' to Restart",
                align="center",
                font=("Courier", 28, "bold"),
            )
        else:
            time.sleep(0.5)
            reset_ball()

    # 4. Paddle Collision 
    if (
        ball.dy < 0
        and (paddle.ycor() - 10 <= ball.ycor() - BALL_RADIUS <= paddle.ycor() + 10)
        and (paddle.xcor() - PADDLE_HALF_WIDTH <= ball.xcor() <= paddle.xcor() + PADDLE_HALF_WIDTH)
    ):
        ball.sety(paddle.ycor() + 10 + BALL_RADIUS)
        ball.dy *= -1

        # Adjust horizontal angle based on where the ball hits the paddle
        offset = (ball.xcor() - paddle.xcor()) / PADDLE_HALF_WIDTH
        ball.dx = offset * (BASE_SPEED * 1.35)

    # 5. Brick Collisions (AABB Overlap Detection)
    for brick in bricks[:]:
        dx = abs(ball.xcor() - brick.xcor())
        dy = abs(ball.ycor() - brick.ycor())

        if dx < (BRICK_WIDTH / 2 + BALL_RADIUS) and dy < (BRICK_HEIGHT / 2 + BALL_RADIUS):
            # Determine whether collision was horizontal or vertical
            overlap_x = (BRICK_WIDTH / 2 + BALL_RADIUS) - dx
            overlap_y = (BRICK_HEIGHT / 2 + BALL_RADIUS) - dy

            if overlap_x < overlap_y:
                ball.dx *= -1
            else:
                ball.dy *= -1

            # Remove brick and update score
            brick.hideturtle()
            bricks.remove(brick)
            score += brick.points
            update_hud()

            # Slightly increase ball speed as bricks are cleared
            ball.dx *= 1.01
            ball.dy *= 1.01
            break  # Only break one brick per frame

    # 6. Win Condition
    if not bricks:
        game_over = True
        msg_turtle.goto(0, 0)
        msg_turtle.write(
            f"YOU WIN! Final Score: {score}\nPress 'R' to Play Again",
            align="center",
            font=("Courier", 24, "bold"),
        )