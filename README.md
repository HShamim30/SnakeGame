# 🐍 Snake Game – Arcade Monster

Snake Game – Arcade Monster is a modern arcade-style snake game developed using **Python and Pygame**.  
This project enhances the classic snake game with **power-ups, hazards, multiple game modes, sound effects, modern UI, and score management**.

It is suitable for **academic projects, mini-projects, final year projects, and game development practice**.

---

## 🎯 Project Description

The game provides an engaging arcade experience through two different modes:
- **Survival Mode** – Endless gameplay focused on survival and high scores.
- **Level Mode** – Structured gameplay with increasing difficulty and obstacles.

The project demonstrates **game logic design, event handling, collision detection, file handling, and modular programming** using Python.

---

## 🎮 Game Modes

### 🔹 Survival Mode
Survival Mode is an endless mode where the player must survive as long as possible.

Features:
- Apples spawn continuously and increase score.
- No obstacles.
- Bombs appear randomly:
  - Touching a bomb results in instant Game Over.
- When snake length reaches **10**, speed becomes **2×**.
- When snake length reaches **15**, a **Magnet power-up** appears:
  - A visible radius is shown around the snake head.
  - Apples inside the radius are automatically eaten.
- When snake length reaches **25**, a **Scissor power-up** appears:
  - Reduces snake length by 10 segments.
- Hitting walls or the snake’s own body causes Game Over.
- Game Over screen provides:
  - Restart
  - Back to Main Menu

---

### 🔹 Level Mode
Level Mode provides structured gameplay with increasing difficulty.

Features:
- Multiple levels.
- Each level requires eating a fixed number of apples.
- Game speed increases with each level.
- Obstacles appear in higher levels.
- Touching an obstacle causes Game Over.
- Snake must avoid walls, obstacles, and itself.
- Total score accumulates across all levels.
- Restarting resets the game to Level 1.

---

## 🧮 Scoring System
- Each apple gives **10 points**.
- Survival Mode and Level Mode have **separate high scores**.
- Top 5 scores are saved automatically.
- Scores remain saved even after restarting the game.

---

## 🎨 Graphics and Sound
- Custom images for:
  - Apple
  - Bomb
  - Magnet
  - Scissor
  - Obstacle
- Sound effects for:
  - Eating apple
  - Bomb explosion
  - Power-up collection
  - Game Over
- Modern UI with panels, glow effects, and buttons.

---

## 🛠️ Requirements

### Software Requirements
- Operating System: Windows / Linux / macOS
- Python Version: **Python 3.9 or higher**
- RAM: Minimum 2 GB
- Disk Space: Minimum 200 MB

### Python Libraries
- pygame

---

## 🔽 How to Clone the Project

```bash
git clone https://github.com/HShamim30/SnakeGame
cd snake-game-arcade-monster

Install required library:

pip install pygame

🎨 Generate Game Assets (One Time Only)

This project includes an automatic asset generator that creates all required images and sounds.

python generate_assets.py


This command will generate all images and sound files required to run the game.

▶️ How to Run the Game
python main.py
