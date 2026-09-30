# Real-Time Flappy Bird Clone

This project is a terminal-based Flappy Bird clone using **Pygame**. It introduces students to interactive game design using object-oriented principles and real-time graphical rendering.

---

### LLM Used 

__ChatGPT__ - Link :- https://chatgpt.com/share/6abd0d04-9afc-83ee-9c98-956e3ac03ebc

## What’s Provided

A partially working version of a Flappy Bird game with:

- A player-controlled bird affected by gravity, with a flap on key/click
- Scrolling pipes with a randomized gap
- Score display

You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Clone the repo or download the project folder.
2. Make sure you have Python 3.10+ installed.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the game:

```bash
python main.py
```


---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Refine Collision Detection

> The bird sometimes clips the edge of a pipe without dying, especially as pipe speed increases. Investigate and enhance collision accuracy so hits are detected consistently.

### Task 2: Implement Game Over Condition

> Add a screen that displays the final score once the bird hits the ground, ceiling, or a pipe, then gracefully waits for input instead of just printing to the console.


### Task 3: Add Replay Option

> After Game Over, allow the user to play again by choosing a difficulty (Easy, Medium, or Hard pipe speed/gap), or exit.


### Task 4: Add Sound Feedback

> Add basic sound effects for flapping, passing a pipe (scoring), and dying.


---

## Expected Behavior

- Bird flaps upward on `Space` or mouse click, and falls due to gravity otherwise
- Pipes spawn at a regular interval and scroll from right to left with a randomized gap
- Score increases by one each time the bird passes a pipe
- Game ends when the bird hits the ground, the ceiling, or a pipe

---

## Folder Structure

```
flappybird-main/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── bird.py
│   └── pipe.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
