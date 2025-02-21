# README_en

## Project Background

This project simulates a turn-based strategy scenario similar to the battle between 10 anti-air infantry and an Apocalypse Tank in Command & Conquer: Red Alert 3. The player controls the infantry units using reinforcement learning algorithms, with the goal of surviving under the tank's crash and attacks and ultimately destroying the tank. The project employs the Q-learning algorithm for training, including complete game logic, a visual interface, and a training framework.
video link :https://drive.google.com/file/d/1eMiAzq4YBNE3Hugr_GHDW3v9E791aPqy/view?usp=sharing

## Code Structure Overview

### Core Modules

| File          | Function Description                                         |
| :------------ | :----------------------------------------------------------- |
| `game5.py`    | Main game entry point, featuring both UI (`start_ui()`) and no UI (`start_no_ui()`) modes. Handles player input, turn流程, and win/lose判定. |
| `tank.py`     | Defines the `Tank` class (HP 75 / Attack 2 / Movement 7) and `TankAI` class. Implements tank movement,碾压, area attacks, and AI decision-making logic. |
| `infantry.py` | Defines the `Infantry` class (HP 8 / Attack 1 / Movement 4). Includes infantry attributes and pre-generated action space `ACTION` (total 41 movement combinations). |
| `panal.py`    | Game interface module. Handles grid drawing, health bars, victory/defeat prompts, and defines battlefield parameters (100x100 grid, CELL=12px). |

### Training System

| File          | Function Description                                         |
| :------------ | :----------------------------------------------------------- |
| `train.py`    | No-interface training script. Includes `Environment` class (environment interaction) and `QLearningAgent` class (Q-table management / policy learning). |
| `train_ui.py` | Training script with a visual interface. Supports dynamic display of the training process and extends the basic training logic. |

## Core Mechanisms (Code Implementation Version)

### Unit Parameters

| Unit              | Attributes                    | Code Values      |
| :---------------- | :---------------------------- | :--------------- |
| Anti-Air Infantry | HP / Movement / Range         | 8 / 4 / 18       |
| Apocalypse Tank   | HP / Attack / Movement / Size | 75 / 2 / 7 / 3x3 |

### Turn Flow

1. **Player Phase**: Infantry executes movement actions selected by the Q-learning strategy.

2. Tank Phase

   :

   - AI decides the movement path (prioritizing approaching the closest surviving infantry).
   - Crushes infantry in the path (immediate death).
   - Automatically attacks targets within range (area attacks not yet implemented).

3. **Environment Settlement**: Checks for win/lose conditions (tank HP reaches zero or all infantry destroyed).

### Key Logic

- **Tank Crush**: Implemented via `Tank.crush()` method, which instantly kills all infantry in a 3x3 area.

- Reward Mechanism

  :

  - +6 reward for successfully attacking the tank.
  - -35 penalty for being crushed.
  - -1 penalty for ineffective movement.

- **State Encoding**: `(dx, dy, hp)` represents the relative position between infantry and tank and the current HP.

## Running Instructions

### Dependencies

```
bash
Copy code
pip install pygame
```

### Startup Methods

- **Direct Game Play**: Run `game5.py` to experience the basic gameplay.
- **No-Interface Training**: Execute `train.py` (need to disable the last pickle save code).
- **Visual Training**: Run `train_ui.py` to observe the learning process.

## File Relationship Diagram

```
Copy codegame5.py (Main Entry) 
├── tank.py # Tank logic 
├── infantry.py # Infantry attributes 
├── panal.py # Interface drawing 
├── train.py # Core training logic 
└── train_ui.py # Training interface extension 
```