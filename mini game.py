import turtle
import time
import random

# -------- Settings --------
DELAY = 0.10          # lower = faster
MOVE_DIST = 20
WIDTH, HEIGHT = 600, 600

# -------- Screen --------
wn = turtle.Screen()
wn.title("Snake 🐍 — Turtle Edition")
wn.bgcolor("#0b132b")
wn.setup(width=WIDTH, height=HEIGHT)
wn.tracer(0)

# -------- Scoreboard --------
score = 0
high_score = 0

pen = turtle.Turtle()
pen.speed(0)
pen.color("#f0f3bd")
pen.penup()
pen.hideturtle()
pen.goto(0, HEIGHT//2 - 40)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 16, "normal"))

# -------- Snake Head --------
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("#5bc0be")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# -------- Food --------
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("#ff595e")
food.penup()
food.goto(0, 100)

# -------- Segments --------
segments = []

# -------- Functions --------
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    x, y = head.xcor(), head.ycor()
    if head.direction == "up":
        head.sety(y + MOVE_DIST)
    elif head.direction == "down":
        head.sety(y - MOVE_DIST)
    elif head.direction == "left":
        head.setx(x - MOVE_DIST)
    elif head.direction == "right":
        head.setx(x + MOVE_DIST)

def update_score():
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 16, "normal"))

def reset_game():
    global score, DELAY
    time.sleep(0.8)
    head.goto(0, 0)
    head.direction = "stop"

    # hide segments off-screen then clear
    for seg in segments:
        seg.goto(1000, 1000)
    segments.clear()

    score = 0
    DELAY = 0.10
    update_score()

# -------- Controls --------
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
# Alternative WASD
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# -------- Game Loop --------
while True:
    wn.update()

    # Border collision
    half_w, half_h = WIDTH // 2 - 10, HEIGHT // 2 - 10
    if (head.xcor() > half_w or head.xcor() < -half_w or
        head.ycor() > half_h or head.ycor() < -half_h):
        reset_game()

    # Food collision
    if head.distance(food) < 18:
        # move food to random spot (grid aligned)
        nx = random.randrange(-half_w, half_w, MOVE_DIST)
        ny = random.randrange(-half_h, half_h, MOVE_DIST)
        food.goto(nx, ny)

        # add new segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("#3a506b")
        new_segment.penup()
        segments.append(new_segment)

        # update score & speed up a bit
        score += 10
        if score > 0 and score % 50 == 0 and DELAY > 0.04:
            DELAY -= 0.01
        if score > high_score:
            high_score = score
        update_score()

    # Move the tail in reverse order
    for idx in range(len(segments)-1, 0, -1):
        x = segments[idx-1].xcor()
        y = segments[idx-1].ycor()
        segments[idx].goto(x, y)

    # Move segment 0 to head
    if segments:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # Self collision
    for seg in segments:
        if seg.distance(head) < 20:
            reset_game()
            break

    time.sleep(DELAY)
