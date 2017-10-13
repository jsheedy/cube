from cube import engine
from cube.engine import Vector3
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

theta = 0
while True:
    theta += 0.05
    renderer.render(hud, scene)
    renderer.delay()
    cube.rotation = Vector3(0, theta, 0)
