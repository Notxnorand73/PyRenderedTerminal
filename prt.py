import time
from typing import Optional

# PyRenderedTerminal - Terminal but Graphical

class Clock:
  def __init__(self, fps: int = 30):
    self.fps = fps
    self.last_tick = time.time()

  def tick(self):
    elapsed = time.time() - self.last_tick
    sleep_time = (1 / self.fps) - elapsed
    if sleep_time > 0:
        time.sleep(sleep_time)
    self.last_tick = time.time()

class Scene:
  def __init__(self, width: int = 24, height: int = 8, bg: str = "."):
    print("\033[2J", end="")
    self.width = width
    self.height = height
    self.bg = bg
    self.scene = [[bg for _ in range(width)] for _ in range(height)]
    self.update()
  def update(self):
    self.scenestr = "\n".join("".join(y) for y in self.scene)
  def render(self):
    self.update()
    print("\033[H" + self.scenestr, end="")
  def draw(self, x: int, y: int, symbol: str):
    if len(str(symbol)) != 1:
      return False
    if not (isinstance(x, int) and isinstance(y, int)):
      return False
    if not (0 <= x < self.width and 0 <= y < self.height):
      return False
    self.scene[y][x] = str(symbol)
    return True
  def clear(self):
    self.scene = [[self.bg for _ in range(self.width)] for _ in range(self.height)]
    self.update()
  def get(self, x, y):
    if 0 <= x < self.width and 0 <= y < self.height:
      return self.scene[y][x]
    return None

def stamp(scene: Scene, x: int, y: int, text: str, transparent_char: Optional[str] = None):
  for idx, i in enumerate(str(text).split("\n")):
    for jdx, j in enumerate(i):
      if j == transparent_char:
        continue
      res = scene.draw(x+jdx, y+idx, j)
      if not res:
        break

def rect(scene: Scene, x: int, y: int, width: int, height: int, char: str):
  for i in range(y, y+height):
    for j in range(x, x+width):
      scene.draw(j, i, char)

def collides(actor1, actor2):
  w1, h1 = len(actor1.sprite.split("\n")[0]), len(actor1.sprite.split("\n"))
  w2, h2 = len(actor2.sprite.split("\n")[0]), len(actor2.sprite.split("\n"))
  return not (actor1.x + w1 <= actor2.x or actor1.x >= actor2.x + w2 or actor1.y + h1 <= actor2.y or actor1.y >= actor2.y + h2)

class Actor:
  def __init__(self, x: int, y: int, spritesheet: dict):
    self.x = x
    self.y = y
    self.spritesheet = spritesheet
    self.sprite = None
  def asset(self, sprite: str):
    if not (sprite in self.spritesheet):
      return False
    self.sprite = self.spritesheet[sprite]
    return True
  def goto(self, x: int, y: int):
    self.x = x
    self.y = y
  def move(self, dx: int, dy: int):
    self.x += dx
    self.y += dy
  def add(self, sprite: str, name: str):
    self.spritesheet[name] = sprite
  def clone(self):
    return Actor(self.x, self.y, self.spritesheet.copy())
  def stamp(self, scene: Scene, transparent_char: str = " "):
    if self.sprite is None:
      return False
    stamp(scene, self.x, self.y, self.sprite, transparent_char)
  
