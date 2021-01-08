# SPACE INVADERS - by Giacomo Tampella

# tampella@icloud.com

import turtle
import os
import math
import random
import platform

# IF ON WINDOWS, YOU IMPORT WINSOUND, OR BETTER YET, JUST USE LINUX
if platform.system() == "Windows":
    try: 
        import winsound
    except:
        print("Winsound module not available.")

# SET UP THE SCREEN
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("bgp_1.gif")
wn.tracer(0)

#  REGISTER THE SHAPES
wn.register_shape("invader.gif")
wn.register_shape("player.gif")

# DRAW BORDER
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# SET THE SCORE TO 0
score = 0

# DRAW THE SCORE
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: {}".format(score)
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

#DRAW THE CREDITS
credit_pen = turtle.Turtle()
credit_pen.color("white")
credit_pen.penup()
credit_pen.setposition(90, -330)
creditstring = "Made by Tampella Giacomo"
credit_pen.write(creditstring, False, align="left", font=("Times New Roman", 14, "normal"))
credit_pen.hideturtle()

# CREATE THE PLAYER TURTLE
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)
player.speed = 0

# CHOOSE A NUMBER OF ENEMIES
number_of_enemies = 30
# CREATE AN EMPTY LIST OF ENEMIES
enemies = []

# ADD ENEMIES TO THE LIST
for i in range(number_of_enemies):
    # CREATE THE ENEMY
    enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_number = 0

for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = enemy_start_x + (50 * enemy_number)
    y = enemy_start_y
    enemy.setposition(x, y)
    # UPDATE THE ENEMY NUMBER
    enemy_number += 1
    if enemy_number == 10:
        enemy_start_y -= 50
        enemy_number = 0

enemyspeed = 0.1

# CREATE THE PLAYER'S BULLET
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 1.2

# DEFINE BULLET STATE
# READY - READY TO FIRE
# FIRE - BULLET IS FIRING
bulletstate = "ready"

# MOVE THE PLAYER LEFT AND RIGHT
def move_left():
    player.speed = -0.6

def move_right():
    player.speed = 0.6

def move_player():
    x = player.xcor()
    x += player.speed
    if x < -280:
        x = -280
    player.setx(x)
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    # DECLARE BULLETSTATE AS A GLOBAL IF IT NEEDS CHANGED
    global bulletstate
    if bulletstate == "ready":
        play_sound("laser.wav")
        bulletstate = "fire"
        # MOVE THE BULLET TO THE JUST ABOVE THE PLAYER
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()
        
def isCollision(t1, t2):
    # distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    distance = t1.distance(t2)
    if distance < 15:
        return True
    else:
        return False

def play_sound(sound_file, time = 0):
    # WINDOWS
    if platform.system() == "Windows":
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)
    # LINUX
    elif platform.system == "Linux":
        os.system("aplay -q {}&".format(sound_file))
    # MAC
    else:
        os.system("afplay {}&".format(sound_file))

    # REPEAT SOUND
    if time > 0:
        turtle.ontimer(lambda: play_sound(sound_file, time), t = int(time * 1000))
    

# CREATE KEYBOARD BINDINGS
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

# PLAY BACKGROUND MUSIC
# play_sound("bgm.mp3", 119)

# MAIN GAME LOOP
while True:
    wn.update()
    move_player()

    #creditstring = "Made by Tampella Giacomo"
    #credit_pen.write(creditstring, False, align="left", font=("Times New Roman", 14, "normal"))

    for enemy in enemies:
        # MOVE THE ENEMY
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # MOVE THE ENEMY BACK AND DOWN
        if enemy.xcor() > 280:
            # MOVE ALL ENEMIES DOWN
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # CHANGE ENEMY DIRECTION
            enemyspeed *= -1
            
        if enemy.xcor() < -280:
            # MOVE ALL ENEMIES DOWN
            for e in enemies: 
                y = e.ycor()
                y -= 40
                e.sety(y)
            # CHANGE ENEMY DIRECTION
            enemyspeed *= -1

        # CHEK FO A COLLISION BETWEEN THE BULLET AND THE ENEMY
        if isCollision(bullet, enemy):
            play_sound("explosion.wav")
            # RESET THE BULLET
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            # RESET THE ENEMY
            enemy.setposition(0, 10000)
            # UPDATE THE SCORE
            score += 10
            scorestring = "Score: {}".format(score)
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
            

        if isCollision(player, enemy):
            play_sound("explosion.wav")
            player.hideturtle()
            enemy.hideturtle()
            print ("Game Over")
            break

    # MOVE THE BULLET
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # CHECK TO SEE IF THE BULLET HAS GONE TO THE TOP
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

    # WIN
    if score == 300:
        print ("YOU KILLED ALL THE ENEMIES!")
        break


