import turtle
import random
import math
import os

# config
WIDTH, HEIGHT = 800, 600
HALF_W, HALF_H = WIDTH // 2, HEIGHT // 2
HIGH_SCORE_FILE = "highscore.txt"

DIFFICULTIES = {
    "1": {"name": "EASY", "speed_mult": 0.75, "spawn_mult": 0.7},
    "2": {"name": "NORMAL", "speed_mult": 1.0, "spawn_mult": 1.0},
    "3": {"name": "HARD", "speed_mult": 1.4, "spawn_mult": 1.6},
}

WEAPON_COOLDOWN = {"normal": 15, "rapid": 6, "triple": 15, "mega": 12}

ENEMY_TYPES = {
    "normal": {"shape": "circle", "color": "#745C4E", "speed": 2.0, "points": 10, "health": 1},
    "fast": {"shape": "triangle", "color": "#5C7148", "speed": 4.0, "points": 20, "health": 1},
    "tank": {"shape": "square", "color": "#654E74", "speed": 1.0, "points": 30, "health": 3},
    "zigzag": {"shape": "diamond", "color": "#4E6274", "speed": 2.2, "points": 25, "health": 1},
}

POWERUP_TYPES = {
    "rapid": {"color": "#E7D89C", "label": "Rapid Fire"},
    "triple": {"color": "#9C7CE7", "label": "Triple Shot"},
    "mega": {"color": "#E76A6A", "label": "Mega Shot"},
    "shield": {"color": "#6AAEE7", "label": "Shield"},
    "health": {"color": "#7CE79C", "label": "+1 Life"},
}


# screen
screen = turtle.Screen()
screen.setup(width=WIDTH, height=HEIGHT)
screen.bgcolor("#171719")
screen.title("Space Shooter V5")
screen.tracer(0)

screen.register_shape("diamond", ((0, 14), (14, 0), (0, -14), (-14, 0)))
screen.register_shape("boss", ((0, 45), (45, 15), (30, -45), (-30, -45), (-45, 15)))


#high score 
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                return int(f.read().strip())
        except (ValueError, OSError):
            return 0
    return 0


def save_high_score(value):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(value))
    except OSError:
        pass


#stary background
class Star:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.color("#DDD8D8")
        self.turtle.shapesize(random.choice([0.1, 0.1, 0.2]))
        self.turtle.penup()
        self.speed = random.uniform(1, 3)
        self.reset(first=True)

    def reset(self, first=False):
        x = random.randint(-HALF_W + 10, HALF_W - 10)
        y = random.randint(-HALF_H + 10, HALF_H - 10) if first else HALF_H + 5
        self.turtle.goto(x, y)

    def move(self):
        self.turtle.sety(self.turtle.ycor() - self.speed)
        if self.turtle.ycor() < -HALF_H - 5:
            self.reset()

#player
class Player:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.shape("triangle")
        self.turtle.penup()
        self.turtle.setheading(90)
        self.reset()

    def reset(self):
        self.turtle.goto(0, -250)
        self.turtle.showturtle()
        self.health = 3
        self.max_health = 3
        self.weapon = "normal"
        self.weapon_timer = 0
        self.shield = False
        self.shoot_cooldown = 0
        self.invincible_timer = 0
        self._update_color()

    def move_left(self):
        x = self.turtle.xcor()
        if x > -HALF_W + 30:
            self.turtle.setx(x - 25)

    def move_right(self):
        x = self.turtle.xcor()
        if x < HALF_W - 30:
            self.turtle.setx(x + 25)

    def set_weapon(self, weapon, duration=300):
        self.weapon = weapon
        self.weapon_timer = duration

    def take_damage(self):
        """Returns True if a life was actually lost."""
        if self.invincible_timer > 0:
            return False
        if self.shield:
            self.shield = False
            self.invincible_timer = 40
            self._update_color()
            return False
        self.health -= 1
        self.invincible_timer = 60
        return True

    def _update_color(self):
        self.turtle.color("#6AAEE7" if self.shield else "#89A6B8")

    def update(self):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            self.turtle.showturtle() if self.invincible_timer % 10 < 5 else self.turtle.hideturtle()
            if self.invincible_timer == 0:
                self.turtle.showturtle()
        if self.weapon_timer > 0:
            self.weapon_timer -= 1
            if self.weapon_timer == 0:
                self.weapon = "normal"
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

#bullet
class Bullet:
    def __init__(self, x, y, dx=0, color="#E7CB9C", damage=1, big=False):
        self.turtle = turtle.Turtle()
        self.turtle.shape("square")
        self.turtle.color(color)
        size = (1.0, 2.0) if big else (0.5, 1.5)
        self.turtle.shapesize(stretch_wid=size[0], stretch_len=size[1])
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.dx = dx
        self.dy = 15
        self.damage = damage

    def move(self):
        self.turtle.setx(self.turtle.xcor() + self.dx)
        self.turtle.sety(self.turtle.ycor() + self.dy)

    def offscreen(self):
        return self.turtle.ycor() > HALF_H + 20 or abs(self.turtle.xcor()) > HALF_W + 20

    def remove(self):
        self.turtle.hideturtle()


#enemybullet
class EnemyBullet:
    def __init__(self, x, y):
        self.turtle = turtle.Turtle()
        self.turtle.shape("square")
        self.turtle.color("#E76A6A")
        self.turtle.shapesize(stretch_wid=0.5, stretch_len=1.5)
        self.turtle.setheading(90)
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.dy = -8

    def move(self):
        self.turtle.sety(self.turtle.ycor() + self.dy)

    def offscreen(self):
        return self.turtle.ycor() < -HALF_H - 20

    def remove(self):
        self.turtle.hideturtle()


#enemy
class Enemy:
    def __init__(self, etype, x, y):
        info = ENEMY_TYPES[etype]
        self.type = etype
        self.color = info["color"]
        self.turtle = turtle.Turtle()
        self.turtle.shape(info["shape"])
        self.turtle.color(info["color"])
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.base_speed = info["speed"]
        self.points = info["points"]
        self.health = info["health"]
        self.zigzag_dir = random.choice([-1, 1])
        self.zigzag_timer = random.randint(20, 40)

    def move(self, speed_mult):
        speed = self.base_speed * speed_mult
        self.turtle.sety(self.turtle.ycor() - speed)
        if self.type == "zigzag":
            self.zigzag_timer -= 1
            if self.zigzag_timer <= 0:
                self.zigzag_dir *= -1
                self.zigzag_timer = random.randint(20, 40)
            x = self.turtle.xcor() + self.zigzag_dir * 3
            x = max(-HALF_W + 20, min(HALF_W - 20, x))
            self.turtle.setx(x)

    def hit(self, damage=1):
        self.health -= damage
        return self.health <= 0

    def remove(self):
        self.turtle.hideturtle()


#boss
class Boss:
    def __init__(self, level):
        self.turtle = turtle.Turtle()
        self.turtle.shape("boss")
        self.turtle.color("#8B3A3A")
        self.turtle.penup()
        self.turtle.goto(0, HALF_H + 60)
        self.max_health = 20 + level * 8
        self.health = self.max_health
        self.direction = random.choice([-1, 1])
        self.speed = 3
        self.shoot_timer = 0
        self.points = 200
        self.entering = True

        self.bar_bg = turtle.Turtle()
        self.bar_bg.hideturtle()
        self.bar_bg.penup()
        self.bar_bg.color("#3A3A3A")

        self.bar_fg = turtle.Turtle()
        self.bar_fg.hideturtle()
        self.bar_fg.penup()
        self.bar_fg.color("#E76A6A")

    def move(self):
        if self.entering:
            if self.turtle.ycor() > 200:
                self.turtle.sety(self.turtle.ycor() - 2)
            return
        x = self.turtle.xcor() + self.direction * self.speed
        if x > HALF_W - 60 or x < -HALF_W + 60:
            self.direction *= -1
        self.turtle.setx(self.turtle.xcor() + self.direction * self.speed)
        self.shoot_timer += 1

    def should_shoot(self):
        if not self.entering and self.shoot_timer > 45:
            self.shoot_timer = 0
            return True
        return False

    def hit(self, damage=1):
        self.health -= damage
        return self.health <= 0

    def draw_health_bar(self):
        bar_w = 200
        x = self.turtle.xcor() - bar_w / 2
        y = self.turtle.ycor() + 55

        self.bar_bg.clear()
        self.bar_bg.penup()
        self.bar_bg.goto(x, y)
        self.bar_bg.pendown()
        self.bar_bg.pensize(6)
        self.bar_bg.setheading(0)
        self.bar_bg.forward(bar_w)
        self.bar_bg.penup()

        pct = max(0, self.health / self.max_health)
        self.bar_fg.clear()
        self.bar_fg.penup()
        self.bar_fg.goto(x, y)
        self.bar_fg.pendown()
        self.bar_fg.pensize(5)
        self.bar_fg.setheading(0)
        self.bar_fg.forward(bar_w * pct)
        self.bar_fg.penup()

    def remove(self):
        self.turtle.hideturtle()
        self.bar_bg.clear()
        self.bar_fg.clear()
        self.bar_bg.hideturtle()
        self.bar_fg.hideturtle()


#powerup
class PowerUp:
    def __init__(self, x, y, ptype):
        info = POWERUP_TYPES[ptype]
        self.type = ptype
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.color(info["color"])
        self.turtle.shapesize(0.8)
        self.turtle.penup()
        self.turtle.goto(x, y)

    def move(self):
        self.turtle.sety(self.turtle.ycor() - 3)

    def offscreen(self):
        return self.turtle.ycor() < -HALF_H - 20

    def remove(self):
        self.turtle.hideturtle()


#particle
class Particle:
    def __init__(self, x, y, color):
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.color(color)
        self.turtle.shapesize(0.3)
        self.turtle.penup()
        self.turtle.goto(x, y)
        angle = random.uniform(0, 360)
        speed = random.uniform(2, 6)
        self.dx = speed * math.cos(math.radians(angle))
        self.dy = speed * math.sin(math.radians(angle))
        self.life = random.randint(10, 20)

    def move(self):
        self.turtle.setx(self.turtle.xcor() + self.dx)
        self.turtle.sety(self.turtle.ycor() + self.dy)
        self.life -= 1

    def dead(self):
        return self.life <= 0

    def remove(self):
        self.turtle.hideturtle()


#game state
state = "menu"  
score = 0
level = 1
next_boss_score = 500
high_score = load_high_score()
difficulty_key = "2"

stars = [Star() for _ in range(60)]
player = Player()
bullets = []
enemy_bullets = []
enemies = []
powerups = []
particles = []
boss = None

level_announce_timer = 0

#displays
score_display = turtle.Turtle()
score_display.hideturtle()
score_display.color("#E8FDFF")
score_display.penup()
score_display.goto(-380, 260)


level_display = turtle.Turtle()
level_display.hideturtle()
level_display.color("#E8FDFF")
level_display.penup()
level_display.goto(-160, 260)

high_display = turtle.Turtle()
high_display.hideturtle()
high_display.color("#E8FDFF")
high_display.penup()
high_display.goto(30, 260)

health_display = turtle.Turtle()
health_display.hideturtle()
health_display.color("#E8FDFF")
health_display.penup()
health_display.goto(220, 260)

weapon_display = turtle.Turtle()
weapon_display.hideturtle()
weapon_display.color("#E7D89C")
weapon_display.penup()
weapon_display.goto(220, 230)

menu_display = turtle.Turtle()
menu_display.hideturtle()
menu_display.penup()

announce_display = turtle.Turtle()
announce_display.hideturtle()
announce_display.color("#E7D89C")
announce_display.penup()
announce_display.goto(0, 150)

gameover_display = turtle.Turtle()
gameover_display.hideturtle()
gameover_display.color("red")
gameover_display.penup()
gameover_display.goto(0, 30)

restart_display = turtle.Turtle()
restart_display.hideturtle()
restart_display.color("white")
restart_display.penup()
restart_display.goto(0, -30)

pause_display = turtle.Turtle()
pause_display.hideturtle()
pause_display.color("white")
pause_display.penup()
pause_display.goto(0, 0)


def update_ui():
    score_display.clear()
    score_display.write(f"Score: {score}", font=("Arial", 14, "normal"))
    level_display.clear()
    level_display.write(f"Level: {level}", font=("Arial", 14, "normal"))
    high_display.clear()
    high_display.write(f"High: {high_score}", font=("Arial", 14, "normal"))
    health_display.clear()
    health_display.write(f"Health: {'❤ ' * player.health}", font=("Arial", 14, "normal"))
    weapon_display.clear()
    label = {"normal": "Normal", "rapid": "Rapid Fire", "triple": "Triple Shot", "mega": "Mega Shot"}[player.weapon]
    weapon_display.write(f"Weapon: {label}", font=("Arial", 11, "normal"))


def draw_menu():
    menu_display.clear()
    menu_display.goto(0, 90)
    menu_display.color("#89A6B8")
    menu_display.write("SPACE SHOOTER", align="center", font=("Arial", 32, "bold"))
    menu_display.goto(0, 40)
    menu_display.color("#E8FDFF")
    menu_display.write("Press SPACE to Start", align="center", font=("Arial", 18, "normal"))
    menu_display.goto(0, 5)
    menu_display.write(f"Difficulty: {DIFFICULTIES[difficulty_key]['name']}  (press 1 / 2 / 3 to change)", align="center", font=("Arial", 13, "normal"))
    menu_display.goto(0, -35)
    menu_display.write("Arrow keys move   SPACE shoot   P pause", align="center", font=("Arial", 13, "normal"))
    menu_display.goto(0, -60)
    menu_display.write("Collect power-ups for shields and better weapons!", align="center", font=("Arial", 13, "normal"))
    menu_display.goto(0, -100)
    menu_display.write(f"High Score: {high_score}", align="center", font=("Arial", 16, "bold"))


draw_menu()


#helpers
def collision(t1, t2):
    return t1.distance(t2) < 20


def spawn_explosion(x, y, color, count=8):
    for _ in range(count):
        particles.append(Particle(x, y, color))


def enemy_weights_for_level(lvl):
    return {
        "normal": 5,
        "fast": 3,
        "tank": min(1 + lvl // 3, 4),
        "zigzag": min(1 + lvl // 2, 4),
    }


def spawn_enemy():
    weights = enemy_weights_for_level(level)
    etype = random.choices(list(weights.keys()), weights=list(weights.values()))[0]
    x = random.randint(-HALF_W + 40, HALF_W - 40)
    y = random.randint(HALF_H - 150, HALF_H - 20)
    enemies.append(Enemy(etype, x, y))


def maybe_drop_powerup(x, y):
    if random.randint(1, 8) == 1:
        ptype = random.choice(list(POWERUP_TYPES.keys()))
        powerups.append(PowerUp(x, y, ptype))


def apply_powerup(ptype):
    if ptype == "rapid":
        player.set_weapon("rapid", 300)
    elif ptype == "triple":
        player.set_weapon("triple", 300)
    elif ptype == "mega":
        player.set_weapon("mega", 300)
    elif ptype == "shield":
        player.shield = True
        player._update_color()
    elif ptype == "health":
        player.health = min(player.max_health + 2, player.health + 1)



#input
def move_left():
    if state == "playing":
        player.move_left()


def move_right():
    if state == "playing":
        player.move_right()


def shoot():
    if state != "playing" or player.shoot_cooldown > 0:
        return
    player.shoot_cooldown = WEAPON_COOLDOWN[player.weapon]
    x, y = player.turtle.xcor(), player.turtle.ycor() + 15
    if player.weapon == "triple":
        bullets.append(Bullet(x, y, dx=0))
        bullets.append(Bullet(x, y, dx=-6))
        bullets.append(Bullet(x, y, dx=6))
    elif player.weapon == "mega":
        bullets.append(Bullet(x, y, dx=0, color="#E76A6A", damage=3, big=True))
    else:
        bullets.append(Bullet(x, y, dx=0))


def select_difficulty(key):
    global difficulty_key
    if state == "menu":
        difficulty_key = key
        draw_menu()


def handle_space():
    if state == "menu":
        start_game()
    elif state == "playing":
        shoot()


def toggle_pause():
    global state
    if state == "playing":
        state = "paused"
        pause_display.clear()
        pause_display.write("PAUSED — press P to resume", align="center", font=("Arial", 18, "bold"))
    elif state == "paused":
        state = "playing"
        pause_display.clear()


def restart():
    if state == "gameover":
        start_game()


#game flow
def start_game():
    global state, score, level, next_boss_score, boss
    for lst in (enemies, bullets, enemy_bullets, powerups, particles):
        for obj in lst:
            obj.remove()
        lst.clear()
    if boss is not None:
        boss.remove()
        boss = None

    menu_display.clear()
    gameover_display.clear()
    restart_display.clear()
    announce_display.clear()

    player.reset()
    score = 0
    level = 1
    next_boss_score = 500
    state = "playing"
    update_ui()

    for _ in range(5):
        spawn_enemy()


def end_game():
    global state, high_score
    state = "gameover"
    if score > high_score:
        high_score = score
        save_high_score(high_score)
    update_ui()
    gameover_display.write("GAME OVER", align="center", font=("Arial", 32, "bold"))
    restart_display.write("Press R to return to Restart", align="center", font=("Arial", 16, "normal"))


def check_level_up():
    global level, level_announce_timer
    new_level = 1 + score // 150
    if new_level != level:
        level = new_level
        level_announce_timer = 60
        announce_display.clear()
        announce_display.write(f"LEVEL {level}", align="center", font=("Arial", 24, "bold"))



#main loop
def game_loop():
    global score, boss, next_boss_score, level_announce_timer

    for star in stars:
        star.move()

    if state == "playing":
        diff = DIFFICULTIES[difficulty_key]
        speed_mult = diff["speed_mult"] * (1 + (level - 1) * 0.12)

        player.update()

        # spawn boss
        if boss is None and score >= next_boss_score:
            boss = Boss(level)
            next_boss_score += 500

        # player bullets
        for b in bullets[:]:
            b.move()
            if b.offscreen():
                b.remove()
                bullets.remove(b)
                continue

            hit_something = False
            for enemy in enemies[:]:
                if collision(b.turtle, enemy.turtle):
                    if enemy.hit(b.damage):
                        score += enemy.points
                        spawn_explosion(enemy.turtle.xcor(), enemy.turtle.ycor(), enemy.color)
                        maybe_drop_powerup(enemy.turtle.xcor(), enemy.turtle.ycor())
                        enemy.remove()
                        enemies.remove(enemy)
                        spawn_enemy()
                        update_ui()
                    hit_something = True
                    break

            if not hit_something and boss is not None and collision(b.turtle, boss.turtle):
                if boss.hit(b.damage):
                    score += boss.points
                    spawn_explosion(boss.turtle.xcor(), boss.turtle.ycor(), "#8B3A3A", count=20)
                    maybe_drop_powerup(boss.turtle.xcor(), boss.turtle.ycor())
                    boss.remove()
                    boss = None
                    update_ui()
                hit_something = True

            if hit_something:
                b.remove()
                if b in bullets:
                    bullets.remove(b)

        # enemies
        for enemy in enemies[:]:
            enemy.move(speed_mult)
            if enemy.turtle.ycor() < -HALF_H + 20:
                enemy.remove()
                enemies.remove(enemy)
                spawn_enemy()
                if player.take_damage():
                    update_ui()
                if player.health <= 0:
                    end_game()
                    return

        # boss
        if boss is not None:
            boss.move()
            boss.draw_health_bar()
            if boss.should_shoot():
                enemy_bullets.append(EnemyBullet(boss.turtle.xcor(), boss.turtle.ycor() - 40))

        # enemy bullets
        for eb in enemy_bullets[:]:
            eb.move()
            if eb.offscreen():
                eb.remove()
                enemy_bullets.remove(eb)
                continue
            if collision(eb.turtle, player.turtle):
                eb.remove()
                enemy_bullets.remove(eb)
                if player.take_damage():
                    update_ui()
                if player.health <= 0:
                    end_game()
                    return

        # powerups
        for p in powerups[:]:
            p.move()
            if p.offscreen():
                p.remove()
                powerups.remove(p)
                continue
            if collision(p.turtle, player.turtle):
                apply_powerup(p.type)
                p.remove()
                powerups.remove(p)
                update_ui()

        # particles
        for particle in particles[:]:
            particle.move()
            if particle.dead():
                particle.remove()
                particles.remove(particle)

        # level announce fade-out
        if level_announce_timer > 0:
            level_announce_timer -= 1
            if level_announce_timer == 0:
                announce_display.clear()

        check_level_up()

        # spawn more regular enemies (paused while boss is up)
        max_enemies = 5 + level // 2
        if boss is None and len(enemies) < max_enemies:
            spawn_chance = max(10, int(40 / diff["spawn_mult"]))
            if random.randint(1, spawn_chance) == 1:
                spawn_enemy()

    screen.update()
    screen.ontimer(game_loop, 20)


#key bindings
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(handle_space, "space")
screen.onkeypress(restart, "r")
screen.onkeypress(restart, "R")
screen.onkeypress(toggle_pause, "p")
screen.onkeypress(toggle_pause, "P")
screen.onkeypress(lambda: select_difficulty("1"), "1")
screen.onkeypress(lambda: select_difficulty("2"), "2")
screen.onkeypress(lambda: select_difficulty("3"), "3")

game_loop()
screen.mainloop()