from cube import engine
from cube.renderer import SDLRenderer

import logging

logging.basicConfig(level=logging.DEBUG)

cube = engine.Cube()
camera = engine.Camera(position=engine.Vector3(0,0,-1))
scene = engine.Scene()
scene.add_object("cube", cube)
scene.add_camera("main camera", camera)

hud = engine.HUD()
renderer = SDLRenderer(delay_interval=50)

while True:
    renderer.render(hud, scene)
    renderer.delay()