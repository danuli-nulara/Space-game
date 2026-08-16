import turtle
import random 

#screen
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.bgcolor("#171719")
screen.title("🚀 Space Shooter")
screen.tracer(0)

game_over=False

#player
player = turtle.Turtle()
player.shape("triangle")
player.color("#89A6B8")
player.penup()
player.setheading(90)
player.goto(0, -250)

#bullets
bullets=[]
def shoot():
    if game_over:
        return 
    
    bullet=turtle.Turtle()
    bullet.shape("square")
    bullet.color("#E7CB9C")
    bullet.shapesize(stretch_wid=0.4,stretch_len=1)
    bullet.penup()
    bullet.goto(player.xcor(),player.ycor()+10)
    bullets.append(bullet)

#enemy
enemies=[]
def create_enemy():
    if game_over:
        return
    enemy=turtle.Turtle()
    enemy.shape("circle")
    enemy.color("#745C4E")
    enemy.penup()

    x=random.randint(-350,350)
    y=random.randint(100,250)

    enemy.goto(x,y)
    enemies.append(enemy)

for _ in range(5):
    create_enemy()

#score
score=0
score_display=turtle.Turtle()
score_display.color("#E8FDFF")
score_display.penup()
score_display.hideturtle()
score_display.goto(-350, 260)
score_display.write(f"Score: {score}", align="center", font=("Arial", 16, "normal"))

#lives
lives=3
lives_display=turtle.Turtle()
lives_display.color("#E8FDFF")
lives_display.penup()
lives_display.hideturtle()
lives_display.goto(250, 260)
lives_display.write(f"Lives: {lives}", align="center", font=("Arial", 16, "normal"))

#game over
game_over_display=turtle.Turtle()
game_over_display.hideturtle()
game_over_display.color('red')
game_over_display.penup()
game_over_display.goto(0,30)

#restart display
restart_display=turtle.Turtle()
restart_display.hideturtle()
restart_display.color('white')
restart_display.penup()
restart_display.goto(0, -30)

def show_game_over():
    global game_over
    game_over=True
    game_over_display.write("GAME OVER", align="center", font=("Arial", 24, "bold"))
    restart_display.write("Press 'R' to Restart", align="center", font=("Arial", 16, "normal"))


#move left
def move_left():
    x = player.xcor()

    if x > -370:
        player.setx(x - 20)

#move right
def move_right():
    x = player.xcor()

    if x < 370:
        player.setx(x + 20)

#collision
def collision(obj01,obj02):
    distance=obj01.distance(obj02)
    return distance<20

#loss life
def lose_life(enemy):
    global lives
    enemy.hideturtle()
    enemies.remove(enemy)
    lives -= 1
    lives_display.clear()
    lives_display.write(f"Lives: {lives}", align="center", font=("Arial", 16, "normal"))
    

    if lives <= 0:
        show_game_over()

#keyboard
screen.listen()

screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(shoot, "space")

#game_loop
def game_loop():
    global score

    #move bullets
    for bullet in bullets[:]:
        bullet.sety(bullet.ycor() + 15)

        #remove bullets that go off the screen
        if bullet.ycor() > 300:
            bullet.hideturtle()
            bullets.remove(bullet)
            continue

        #checkcollision with enemies
        for enemy in enemies[:]:
            if collision(bullet, enemy):
                bullet.hideturtle()
                enemy.hideturtle()
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                score_display.clear()
                score_display.write(f"Score: {score}", align="center", font=("Arial", 16, "normal"))
                create_enemy()
                break

        #move enemies
        for enemy in enemies[:]:
            enemy.sety(enemy.ycor() - 2)
            #Enemy reasches player
            if enemy.ycor() < -230:
                lose_life(enemy)

        #spawn new enemies
        if len(enemies)<5:
            if random.randint(1,50)==1:
                create_enemy()
            
    screen.update()
    screen.ontimer(game_loop, 20)

#restart
def restart():
    global score
    global lives
    global game_over

    if not game_over:
        return

    #remove old enemies
    for enemy in enemies:
        enemy.hideturtle()
    enemies.clear()

    #remove old bullets
    for bullet in bullets:
        bullet.hideturtle()
    bullets.clear()

    #reset values
    score=0
    lives=3
    game_over=False

    #reset player
    player.goto(0,-250)

    #clear messages
    game_over_display.clear()
    restart_display.clear()

    #update score
    score_display.clear()
    score_display.write(f"Score:{score}",font=("Arial",16,"normal"))

    #update lives
    lives_display.clear()
    lives_display.write(f"Lives:[lives]",font=("Arial",16,"normal"))

    #create enemies
    for _ in range(5):
        create_enemy()

screen.onkeypress(restart,'r')

#start game
game_loop()

screen.mainloop()

