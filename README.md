# PyRenderedTerminal (PRT)
**Terminal but Visual**. A lightweight, beginner-friendly graphics engine for Python, designed to help kids and students understand how game engines, layers, and actors work.

## Features
* Actor System: Easy sprite management and movement.

* Scene Layering: Stack different scenes on top of each other.

* Collision Detection: Simple collides() function for game logic.

* Educational: Clean, readable code perfect for classroom learning.

## License
This project is published under the MIT License. Feel free to use, modify, and share it in your own classroom or projects/

## Instalation
Open the terminal and type:
```powershell
pip install git+https://github.com/Notxnorand73/PyRenderedTerminal
```
Check if it is downloaded using:
```powershell
pip show pyrenderedterminal
```
## Quick Start
Copy this into a file (like game.py) to see PRT in action!
```python
from prt import Scene, Actor, Clock
```
### 1. Set up the stage
```python
myscene = Scene(width=30, height=10, bg=".")
myclock = Clock(fps=10)
```
### 2. Create a "Hero" actor
```python
hero_art = {"main": "O"}
player = Actor(5, 5, hero_art)
```
### 2. Game Loop
```python
while True:
    myscene.clear()         # Clear the old frame
    player.move(1, 0)       # Move the hero right
    player.wrap(myscene)    # Wrap around the screen
    
    player.stamp(myscene)   # Draw hero on scene
    myscene.render()        # Show it to the user
    
    myclock.tick()          # Wait for the next frame
```
> [!IMPORTANT]
> In the **Coordinate System:** of PRT, `(0,0)` is the **Top-Left** corner. 
> * **X increases** to the right.
> * **Y increases** going **down**.

Contributing
Want to help make PRT better?
1. Fork the repo.
2. Add a new feature (like a circle drawer).
3. Open a Pull Request.
