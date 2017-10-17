import itertools
import logging
import math

import sdl2

from cube.camera import Camera
from cube.engine import Vector3
from cube.hud import HUD
from cube.objects import Dodecahedron, Cube, Tetrahedron, Octahedron
from cube.renderer import SDLRenderer
from cube.scene import Scene

logging.basicConfig(level=logging.INFO)

scene = Scene()

camera = Camera(position=Vector3(0,4,-20))
camera.look_at(Vector3(0, 0, 0))
scene.add_camera("main camera", camera)


renderer = SDLRenderer(width=1350, height=770, delay_interval=30)
hud = HUD()

for t in itertools.count():
    renderer.render(hud, scene, clear=True, axes=False)
    renderer.delay()

    # camera_x = math.sin(t/20)
    # camera_y = 0  # math.cos(t/20)
    # camera_z = 20-math.cos(t/20)

    # target = 100*Vector3(look_x, look_y, look_z)
    # cube.look_at(target)
    if t % 20 == 0:
        cube = Cube(position=Vector3(0, 0, t/5))
        scene.add_object(f"cube{t}", cube)
        while len(scene.objects) > 20:
            scene.remove_first_object()

    camera.position = Vector3(0, 0, -20+t/5)
    camera.look_at(Vector3(0, 0, 10**100))

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