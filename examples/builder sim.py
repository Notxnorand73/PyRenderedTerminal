from pyrenderedterminal import *

scene = Scene(bg=" ")
player = Actor(5, 3, {"1": ">", "-1": "<"})
player.asset("1")
yvelocity = 0
xvelocity = 0
clock = Clock(15)
world = [[0 for _ in range(scene.width)] for _ in range(scene.height-1)]
while True:
    scene.clear()
    stamp(scene, 0, scene.height-1, "\""*scene.width)
    player.stamp(scene)
    for y, i in enumerate(world):
        for x, j in enumerate(i):
            if j == 0:
                continue
            scene.draw(x, y, "#")

    if scene.get(player.x, player.y+1) in ["\"", "#"] and yvelocity >= 0:
        yvelocity = 0
    else:
        yvelocity += 1
    if scene.get(player.x+xvelocity, player.y) in ["\"", "#"]:
        xvelocity = 0
    if yvelocity % 4 == 0:
        if yvelocity > 0:
            player.move(0, 1)
        elif yvelocity < 0:
            player.move(0, -1)
    player.move(xvelocity, 0)
    player.clamp(scene)
    key = keybind()
    xvelocity = 0
    if key == "a":
        xvelocity = -1
    elif key == "d":
        xvelocity = 1
    elif key == " ":
        if scene.get(player.x, player.y+1) in ["\"", "#"]:
            yvelocity = -12
    elif key == "q":
        if player.spritename == "-1":
            if player.x == 0:
                continue
            world[player.y][player.x-1] = 1
        if player.spritename == "1":
            if player.x == scene.width-1:
                continue
            world[player.y][player.x+1] = 1
    elif key == "e":
        if player.spritename == "-1":
            if player.x == 0:
                continue
            world[player.y][player.x-1] = 0
        if player.spritename == "1":
            if player.x == scene.width-1:
                continue
            world[player.y][player.x+1] = 0
    if xvelocity > 0:
        player.asset("1")
    elif xvelocity < 0:
        player.asset("-1")
    scene.render()
    clock.tick()
