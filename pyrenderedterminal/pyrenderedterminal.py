import time
from typing import Optional
import sys
if sys.platform == "win32":
    import msvcrt
else:
    import select
    import tty
    import termios

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
    print("""
+------------------------------------------------------------+
| PyRenderedTerminal 0.1.2.4 Alpha : Terminal but Visual     |
| Published under the MIT license                            |
+------------------------------------------------------------+
| GitHub: https://github.com/Notxnorand73/PyRenderedTerminal |
+------------------------------------------------------------+
""")
  def update(self):
    self.scenestr = "\n".join("".join(y) for y in self.scene)
  def render(self):
    self.update()
    print("\033[2J\033[H" + self.scenestr, end="")
  def draw(self, x: int, y: int, symbol: str):
    if len(str(symbol)) != 1:
      return False
    if not (isinstance(x, int) and isinstance(y, int)):
      return False
    if not (0 <= x < self.width and 0 <= y < self.height):
      return False
    self.scene[y][x] = str(symbol)
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
      scene.draw(x+jdx, y+idx, j)
    
class Actor:
  def __init__(self, x: int, y: int, spritesheet: dict[str, str]):
    self.x = x
    self.y = y
    self.spritesheet = spritesheet
    self.sprite = None
    self.asset("main")
  def asset(self, sprite: str):
    if not (sprite in self.spritesheet):
      return False
    self.spritename = sprite
    self.sprite = self.spritesheet[sprite]
    self.width = len(max(self.sprite.split("\n"), key=len))
    self.height = len(self.sprite.split("\n"))
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
    newactor = Actor(self.x, self.y, self.spritesheet.copy())
    newactor.asset(self.spritename)
    return newactor
  def stamp(self, scene: Scene, transparent_char: str = " "):
    if self.sprite is None:
      return False
    stamp(scene, self.x, self.y, self.sprite, transparent_char)
  def wrap(self, scene: Scene):
    self.x %= scene.width
    self.y %= scene.height
  def clamp(self, scene: Scene):
    self.x = max(0, min(self.x, scene.width - self.width))
    self.y = max(0, min(self.y, scene.height - self.height))

class Layerer:
  def __init__(self, width: int = 24, height: int = 8, bg: str = "."):
    self.width = width
    self.height = height
    self.bg = bg
    self.layers: list[Scene] = []
    self.scenestr = ""
  def add_layer(self, scene: Scene):
    if scene.width != self.width or scene.height != self.height:
        return False
    self.layers.append(scene)
  def remove_layer(self, scene: Scene):
    self.layers.remove(scene)
  def update(self, transparent_char: Optional[str] = None):
    final = [[self.bg for _ in range(self.width)] for _ in range(self.height)]
    for layer in self.layers:
      for y in range(self.height):
        for x in range(self.width):
          char = layer.get(x, y)
          if char is None:
            continue
          if transparent_char and char == transparent_char:
            continue
          final[y][x] = char
    self.scenestr = "\n".join("".join(row) for row in final)
  def render(self):
    self.update()
    print("\033[2J" + self.scenestr, end="")

def rect(scene: Scene, x: int, y: int, width: int, height: int, char: str):
  for i in range(y, y+height):
    for j in range(x, x+width):
      scene.draw(j, i, char)

def collides(actor1: Actor, actor2: Actor):
  w1, h1 = actor1.width, actor1.height
  w2, h2 = actor2.width, actor2.height
  if (w1 is None) or (w2 is None):
    return False
  return not (actor1.x + w1 <= actor2.x or actor1.x >= actor2.x + w2 or 
              actor1.y + h1 <= actor2.y or actor1.y >= actor2.y + h2)

def keybind():
  if sys.platform == "win32":
    if msvcrt.kbhit():
      return msvcrt.getch().decode("utf-8", errors="ignore")
    return None
  else:
    old_settings = termios.tcgetattr(sys.stdin)
    try:
      tty.setcbreak(sys.stdin.fileno())
      if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        return sys.stdin.read(1)
    finally:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    return None
