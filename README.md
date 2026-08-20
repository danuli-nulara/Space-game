# 🚀 Space Shooter

A small 2D space shooter game built with **Python Turtle**.

This project started as a simple space-shooter experiment and gradually evolved into a more feature-rich version with different enemy types, power-ups, difficulty levels, bosses, a scoring system, and persistent high scores.

## About the Project

The repository contains two versions of the game:

* **`trying_spacegame.py`** — the earlier/simple version used to build the basic game mechanics.
* **`spgame_v2.py`** — the improved version with additional gameplay features and better game structure.

The project was mainly created as a learning project to practice **Python, object-oriented programming, game loops, collision detection, randomization, and basic game-state management**.

## Features

### Core Gameplay

* Player-controlled spaceship
* Animated scrolling star background
* Multiple enemy types
* Shooting and collision detection
* Player health/lives
* Score and level system
* Persistent high score

### Enemy Types

The improved version includes four different enemy types:

| Enemy  | Behavior           | Points | Health |
| ------ | ------------------ | -----: | -----: |
| Normal | Standard enemy     |     10 |      1 |
| Fast   | Moves faster       |     20 |      1 |
| Tank   | Slow but durable   |     30 |      3 |
| Zigzag | Moves side-to-side |     25 |      1 |

Enemy movement and spawning become more challenging as the player's level increases.

##  Weapons & Power-Ups

Power-ups can randomly appear after destroying enemies.

Available power-ups include:

* **Rapid Fire** — reduces the shooting cooldown
* **Triple Shot** — fires three bullets at once
* **Mega Shot** — fires a larger, more powerful bullet
* **Shield** — protects the player from one hit
* **Health** — restores one life

Weapon power-ups are temporary and eventually return the player to the normal weapon.

## Boss Battles

As the player's score increases, a boss appears.

Bosses have:

* A large custom shape
* Their own health bar
* Increasing health based on the current level
* Horizontal movement
* Enemy projectiles
* A higher score reward

The boss system is triggered every **500 points**.

## Difficulty Levels

The game has three difficulty modes:

| Key | Difficulty | Speed | Enemy Spawn |
| --- | ---------- | ----- | ----------- |
| `1` | Easy       | 0.75× | Lower       |
| `2` | Normal     | 1.0×  | Normal      |
| `3` | Hard       | 1.4×  | Higher      |

Difficulty can be selected from the main menu before starting the game.

##  Controls

| Key     | Action                  |
| ------- | ----------------------- |
| `←`     | Move left               |
| `→`     | Move right              |
| `SPACE` | Start game / Shoot      |
| `P`     | Pause / Resume          |
| `R`     | Restart after game over |
| `1`     | Easy difficulty         |
| `2`     | Normal difficulty       |
| `3`     | Hard difficulty         |

##  Game Progression

The game becomes progressively harder as the score increases.

* The player's **level increases every 150 points**.
* Enemy movement speed increases with the level.
* More difficult enemy types become more likely at higher levels.
* The number of enemies that can appear increases.
* Bosses become stronger at higher levels.

## High Score

The game saves the highest score to:

```text
highscore.txt
```

When the game starts, the saved high score is loaded automatically. If a new high score is achieved, it is saved for the next session.

> `highscore.txt` is generated automatically when a new high score is saved.

## Technologies Used

* **Python**
* **Turtle Graphics**
* `random`
* `math`
* `os`

The project does not require external game-development frameworks.

## Project Structure

```text
Space-Shooter/
│
├── trying_spacegame.py   # Earlier/simple version
├── spgame_v2.py          # Improved version
├── highscore.txt         # Generated high-score file
└── README.md
```

##  How to Run

### 1. Install Python

Make sure Python 3 is installed on your computer.

### 2. Clone the repository

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

### 3. Run the game

To run the original version:

```bash
python trying_spacegame.py
```

To run the improved version:

```bash
python spgame_v2.py
```

No additional Python packages are required because the game uses Python's built-in libraries.

## What I Learned

This project helped me practice:

* Object-oriented programming with Python classes
* Game loops
* Keyboard input handling
* Collision detection
* Managing multiple game objects
* Random enemy and power-up spawning
* Game states such as menu, playing, paused, and game over
* Level progression and difficulty scaling
* File handling for persistent high scores
* Basic particle/explosion effects
* Designing and organizing a larger Python program

## 🚀 Future Improvements

Some ideas for future versions:

* Sound effects and background music
* More detailed graphics and animations
* More enemy types
* Multiple boss types
* Better save-game functionality
* Achievements
* Different space environments
* Mouse/controller support
* A proper audio system
* Improved UI and menus

## 📌 Project Status

**Version 2 — Playable**

The project is still a learning project and can be expanded with more gameplay mechanics, visual effects, and audio.

---

### Made with 🐍 Python & 🚀 Turtle

A small project that started simple and kept getting upgraded.
