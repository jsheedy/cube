import itertools

import sdl2

from cube.camera import Camera
from cube.engine import Vector3
from cube.hud import HUD
from cube.objects import Dodecahedron, Cube, Tetrahedron, Octahedron
from cube.renderers import SDLRenderer
from cube.scene import Scene

from cube.hid import drive_obj
from cube.transformations import rotation_matrix


scene = Scene()

camera = Camera(position=Vector3(0,0,-5))
camera.look_at(Vector3(0, 0, 0))
scene.add_camera("main camera", camera)

cube = Cube()
scene.add_object("cube", cube)
hud = HUD()
renderer = SDLRenderer(width=1350, height=770, delay_interval=30)

for t in itertools.count():
    drive_obj(camera)
    renderer.render(hud, scene, clear=True, draw_polys=False)
    cube._rotation_matrix = rotation_matrix(Vector3(t/10000, t/1000, 0))