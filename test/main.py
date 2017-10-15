import logging

import sdl2

from cube.camera import Camera
from cube.engine import Vector3
from cube.hud import HUD
from cube.objects import Dodecahedron, Cube, Tetrahedron, Octahedron
from cube.renderer import SDLRenderer
from cube.scene import Scene

logging.basicConfig(level=logging.INFO)

scene = Scene()

camera = Camera(position=Vector3(2,2,-20))
scene.add_camera("main camera", camera)

# for i in range(-10, 10, 4):
#     for j in range(-10, 10, 4):
#         for k in range(-10, 10, 4):
#             cube = Cube(position=Vector3(2*i, j, k))
#             scene.add_object(f"cube{i}-{j}-{k}", cube)

cube = Cube(position=Vector3(2, 2, 0))
tetrahedron = Tetrahedron(position=Vector3(2,-2, 0))
octahedron = Octahedron(position=Vector3(-2, -2, 0))
dodecahedron = Dodecahedron(position=Vector3(-2, 2, 0))

scene.add_object(f"cube", cube)
scene.add_object(f"tetrahedron", tetrahedron)
scene.add_object(f"octahedron", octahedron)
scene.add_object(f"dodecahedron", dodecahedron)

hud = HUD()
renderer = SDLRenderer(width=1350, height=770, delay_interval=50)

pitch = 0
roll = 0
yaw = 0

while True:
    renderer.render(hud, scene, clear=True)
    renderer.delay()

    pitch += 0.01
    roll += 0.001
    yaw += 0.02
    rot = Vector3(roll, pitch, yaw)
    cube.rotation = rot
    tetrahedron.rotation = rot
    octahedron.rotation = rot
    dodecahedron.rotation = rot

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