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
from cube.events import handle_events
from cube import transformations

logging.basicConfig(level=logging.INFO)

WIDTH = 1350
HEIGHT = 770

scene = Scene()

camera = Camera(position=Vector3(0,0,-1))
camera.look_at(Vector3(0, 0, 0))
scene.add_camera("main camera", camera)

fname = os.path.join(os.path.dirname(__file__), 'data/bunny.ply')

bunnies = []
for i in range(-5, 5, 1):
    bunny = Model.load_ply(fname)
    bunny.position = Vector3(i/5, 0, 0)
    scene.add_object(f"bunny{i}", bunny)
    bunnies.append(bunny)

fname = os.path.join(os.path.dirname(__file__), 'data/teapot.ply')
teapot = Model.load_ply(fname, scale=Vector3(0.02, 0.02, 0.02))
teapot.position = Vector3(0.1, 0, 0)
teapot._rotation_matrix = transformations.rotation_matrix(Vector3(-90, 0, 0))
scene.add_object("teapot", teapot)

renderer = SDLRenderer(width=WIDTH, height=HEIGHT, delay_interval=30)
hud = HUD()

for t in itertools.count():
    for bunny in bunnies:
        bunny._rotation_matrix = transformations.rotation_matrix(Vector3(0, t/50, 0))
    # teapot._rotation_matrix = transformations.rotation_matrix(Vector3(0, t/50, 0))
    renderer.render(hud, scene, clear=True, draw_vertices=False, draw_polys=True)
    renderer.delay()
    handle_events(camera, WIDTH, HEIGHT)