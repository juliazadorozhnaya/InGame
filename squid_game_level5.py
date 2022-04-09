"""One of the levels of the Sqiud Game, which consists in not getting on a broken glass block."""

from ursina import Ursina, window, Entity, invoke, destroy, duplicate, color
from ursina.prefabs.first_person_controller import FirstPersonController
from random import randint


app = Ursina()
window.fullscreen = True
window.color = color.black


player = FirstPersonController(collider="box", jump_duration=0.5)
player.cursor.visible = False
ground = Entity(
    model="plane", texture="vertical_gradient", collider="mesh", scale=(30, 0, 3)
)

pill1 = Entity(
    model="cube", color=color.rgb(227, 62, 126), scale=(0.4, 0.1, 53), z=28, x=-0.7
)
pill2 = duplicate(pill1, x=-3.7)
pill3 = duplicate(pill1, x=0.6)
pill4 = duplicate(pill1, x=3.6)


blocks = []
for i in range(12):
    block = Entity(
        model="cube",
        collider="box",
        color=color.white33,
        position=(2, 0.2, 3 + i * 4),
        scale=(3, 0.1, 2.5),
    )
    block2 = duplicate(block, x=-2.2)
    blocks.append((block, block2, randint(0, 10) > 7, randint(0, 10) > 7))

goal = Entity(color=color.blue, model="cube", z=55, scale=(10, 1, 10))
pillar = Entity(color=color.blue, model="cube", z=58, scale=(1, 15, 1), y=8)


def update():
    """Break random blocks, on which the player stands."""
    for block1, block2, k, n in blocks:
        for x, y in [(block1, k), (block2, n)]:
            if x.intersects() and y:
                invoke(destroy, x, delay=0.1)
                x.fade_out(duration=0.1)


def input(key):
    """Press the 'q' button exits the game."""
    if key == "q":
        quit()


app.run()
