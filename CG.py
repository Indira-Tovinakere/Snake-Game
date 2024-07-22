import turtle
import time
import random

# Load the background image
from PIL import Image

# Open the uploaded image
image_path = "grass.jpg"
bg_image = Image.open(image_path)

# Resize the image to fit the white box area (600x600 pixels)
bg_image = bg_image.resize((600, 600))

# Save it as a GIF image
bg_image_path = "background.gif"
bg_image.save(bg_image_path, "GIF")

# Set up the screen
screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("darkcyan")
screen.setup(width=700, height=700)
screen.tracer(0)  # Turns off the screen updates

# Add background image within the white box area
screen.addshape(bg_image_path)
bg_turtle = turtle.Turtle()
bg_turtle.speed(0)
bg_turtle.shape(bg_image_path)
bg_turtle.penup()
bg_turtle.goto(0, 0)
bg_turtle.stamp()

# Initialize score
score = 0

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("red")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("orange")
food.penup()
food.goto(0, 100)

segments = []

# Pen for score display
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 310)  # Adjusted score display position
pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

# Boundary
boundary = turtle.Turtle()
boundary.speed(0)
boundary.color("red")
boundary.penup()
boundary.goto(-300, -300)
boundary.pendown()
boundary.pensize(4)
for _ in range(4):
    boundary.forward(600)
    boundary.left(90)
boundary.hideturtle()

# Functions to control the snake
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
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Function to end the game
def end_game():
    global running
    running = False
    screen.clear()
    screen.bgcolor("coral")
    pen.goto(0, 0)
    pen.write(f"Game Over! Final Score: {score}", align="center", font=("Times New Roman", 36, "bold"))

# Generate food in a valid position
def generate_food():
    while True:
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        if (x, y) not in [(segment.xcor(), segment.ycor()) for segment in segments]:
            food.goto(x, y)
            break

# Keyboard bindings
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(go_right, "Right")

# Main game loop
running = True
while running:
    screen.update()

    # Check for collision with food
    if head.distance(food) < 20:
        generate_food()  # Regenerate food in a valid position
        
        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("maroon")
        new_segment.penup()
        segments.append(new_segment)
        
        # Increase the score
        score += 10
        pen.clear()
        pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

    # Move the end segments first in reverse order
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # Check for collision with the wall
    if head.xcor() > 280 or head.xcor() < -280 or head.ycor() > 280 or head.ycor() < -280:
        end_game()
        break

    # Check for collision with the body
    for segment in segments:
        if segment.distance(head) < 20:
            end_game()
            break

    time.sleep(0.1)

screen.mainloop()