# Connect 4 AI Game 🎮🧠

A Python implementation of the classic **Connect 4** game featuring:
- **Two-player mode**
- **Single-player mode** against an AI using **Minimax** (with and without Alpha-Beta pruning)
- **Q-Learning agent** (training and inference)

The game includes beautiful fonts and visuals using **Pygame** and is easy to extend or improve for AI experimentation.

---

## 🧠 AI Features

- **Minimax Algorithm** with heuristic evaluation for offensive and defensive plays.
- **Alpha-Beta Pruning** for optimized decision-making in hard mode.
- **Q-Learning Agent** for reinforcement learning-based gameplay.

---

## 📂 Project Structure

```
├── assets/                  # Custom fonts used in the game
│   ├── DragonHunter-9Ynxj.otf
│   └── ...
├── build_q_table.py         # Script to build the Q-table for the RL agent
├── game.py                  # Entry point for starting the game
├── minimax.py               # Minimax AI implementation
├── q_learning.py            # Q-learning training and game logic
├── single_player.py         # Shared logic for single-player mode
├── two_players.py           # Local two-player mode implementation
```

---

## 🚀 Getting Started

### ✅ Prerequisites

Make sure you have Python 3 installed along with the required packages:

```bash
pip install pygame numpy
```

---

### ▶️ Running the Game

#### Start the game with Minimax AI:

```bash
python minimax.py
```

#### Train or test Q-learning agent:

```bash
python q_learning.py
```

#### Build Q-table:

```bash
python build_q_table.py
```

#### Play with a friend (2-player mode):

```bash
python two_players.py
```

---

## 🧮 Minimax AI Details

- Evaluates each potential move using a scoring function.
- Takes into account:
  - Center control
  - Two/Three/Four-in-a-row formations
  - Blocking opponent's winning chances
- Two difficulty levels:
  - **Easy:** Lower depth, basic decision tree
  - **Hard:** Alpha-beta pruning and deeper search

---

## 🤖 Q-Learning Agent

- Uses a state-action value table (Q-table) for learning
- Can be trained over multiple episodes using `build_q_table.py`

---

## 🎨 Fonts & Design

Custom fonts located in the `assets/` folder are used for enhancing the visual aesthetics of the game.


---

## 📃 License

This project is open-source and free to use under the MIT License.

