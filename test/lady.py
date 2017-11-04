import itertools
import logging
import math
import os

import sdl2

from cube.camera import Camera
from cube.engine import Vector3
from cube.hud import HUD
from cube.model import Model
from cube.objects import Dodecahedron, Cube, Tetrahedron, Octahedron
from cube.renderer import SDLRenderer
from cube.scene import Scene

logging.basicConfig(level=logging.INFO)

scene = Scene()

camera = Camera(position=Vector3(0,0,-70))
camera.look_at(Vector3(0, 0, 0))
scene.add_camera("main camera", camera)

fname = os.path.join(os.path.dirname(__file__), 'data/kscan3d-lady-ascii.ply')
lady = Model.load_ply(fname)
scene.add_object('lady', lady)

renderer = SDLRenderer(width=1350, height=770, delay_interval=30)
hud = HUD()

for t in itertools.count():
    renderer.render(hud, scene, clear=True)
    renderer.delay()

    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.scancode == sdl2.SDL_SCANCODE_DOWN:
                camera.rotation.y += .1
            elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_UP:
                camera.rotation.y -= .1
            elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_LEFT:
                camera.rotation.x += .1
            elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_RIGHT:
                camera.rotation.x -= .1
            elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_S:
                camera.position.z -= 5
            elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_W:
                camera.position.z += 5
            elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_Q:
                raise Exception("quit")
        if event.type == sdl2.SDL_QUIT:
            raise Exception("quit")