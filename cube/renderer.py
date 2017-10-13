import logging
import math

import numpy as np
import sdl2
import sdl2.ext
from sdl2 import sdlgfx


logger = logging.getLogger(__name__)


class Renderer():
    """ renders a Scene """

    pass


class SDLRenderer(Renderer):
    def __init__(self, width=800, height=600, f=800, window_title="CUBE", delay_interval=10):
        self.width = width
        self.height = height
        self.f = f
        self.frame = 0
        sdl2.ext.init()

        # sdl2.mouse.SDL_ShowCursor(0)
        flags = 0
        # flags = sdl2.SDL_RENDERER_SOFTWARE
        self.window = sdl2.ext.Window(window_title, flags=flags, size=(width, height))
        self.window.show()
        # self.surface = self.window.get_surface()
        self.context = sdl2.ext.Renderer(self.window)

        self.delay_interval = delay_interval

    def draw_axes(self, length=1, thickness=3):

        axes = np.matrix([
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [1, 1, 1, 1],
        ], dtype=np.float)

        axes[:3, :] *= length

        points = [tuple(x) for x in self.vertices_to_screen(self.M * axes).T.A]
        if len(points) < 4:
            return
        pairs = (
            ((255, 0, 0), points[0], points[1]),
            ((0, 255, 0), points[0], points[2]),
            ((0, 0, 255), points[0], points[3]),
        )

        for color, p1, p2 in pairs:
            try:
                cv2.line(target, p1, p2, color, thickness, cv2.LINE_AA)
            except OverflowError as e:
                pass

    def draw_hud(self, hud):
        surface = self.surface
        pixels = sdl2.ext.pixels2d(surface)
        color = int(127*(math.sin(self.frame)+1)) << 16
        h, w = pixels.shape
        pixels[0:10, :] = color
        pixels[h-10:h, :] = color
        pixels[:, 0:10] = color
        pixels[:, w-10:w] = color

    def vertices_to_screen(self, scene, vertices):
        camera_matrix = self.camera_matrix()
        transformed_vertices = scene.main_camera.R.I * scene.main_camera.T.I * vertices
        # mask = (vertices[2, :] > 0).A[0]
        # forward_vertices = vertices[:, mask]
        points = camera_matrix * transformed_vertices  # forward_vertices breaks lines

        # perspective
        points = points[:2, :] / points[2, :]

        points_int = points.astype(np.uint8)
        return points_int

    def render(self, hud, scene):

        self.frame += 1
        context = self.context
        context.clear(0)
        sdlgfx_green = 0xff00ff00  # 0xff << 16 + 0xff  # RGBA
        # sdlgfx_green = 0xffffffff  # 0xff << 16 + 0xff  # RGBA
        for name, obj in scene.objects.items():
            obj.update()
            points = self.vertices_to_screen(scene, obj.transformed_vertices)
            logger.debug(f"rendering {name}")

            n_points = points.shape[1]
            for i in range(n_points):
                x1 = points[0, i]
                y1 = points[1, i]
                logger.debug(f"rendering {(x1,y1)}")
                sdlgfx.filledCircleColor(context.sdlrenderer, x1, y1, 3, sdlgfx_green)

            for p1, p2 in obj.edges:
                x1 = points[0, p1]
                y1 = points[1, p1]

                x2 = points[0, p2]
                y2 = points[1, p2]

                sdlgfx.aalineColor(context.sdlrenderer, x1, y1, x2, y2, sdlgfx_green)

        self.draw_test_grid(context)
        context.present()
        # self.draw_hud(hud)
        self.window.refresh()


    def draw_test_grid(self, context):
        c = 0xffffffff
        # for x in range(0, self.width, 10):
        #     for y in range(0, self.height, 10):
        #         sdlgfx.filledCircleColor(context.sdlrenderer, x, y, 1, c)
        sdlgfx.filledCircleColor(context.sdlrenderer, 400, 300, 4, c)


    def camera_matrix(self):
        cx = self.width / 2
        cy = self.height / 2
        f = self.f

        return np.matrix([
            [f,  0, cx, 0],
            [0, f, cy, 0],
            [0,  0,  1, 0]
        ], dtype=np.float64)


    def delay(self):
        sdl2.SDL_Delay(self.delay_interval)


    def quit(self):

        sdl2.ext.quit()

