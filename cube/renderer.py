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
    def __init__(self, width=800, height=600, f=100, window_title="CUBE", delay_interval=10):
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

    def draw_hud(self, hud):
        surface = self.surface
        pixels = sdl2.ext.pixels2d(surface)
        color = int( 127*(math.sin(self.frame)+1)) << 16
        h, w = pixels.shape
        pixels[0:10, :] = color
        pixels[h-10:h, :] = color
        pixels[:, 0:10] = color
        pixels[:, w-10:w] = color

    def render(self, hud, scene):

        self.frame += 1

        green = sdl2.ext.Color(100, 255, 100)
        camera_matrix = self.camera_matrix()

        R = scene.main_camera.rotation
        T = scene.main_camera.position
        context = self.context
        context.clear(0)
        sdlgfx_green = 0xff00ff00  # 0xff << 16 + 0xff  # RGBA
        # sdlgfx_green = 0xffffffff  # 0xff << 16 + 0xff  # RGBA
        for name, obj in scene.objects.items():
            obj.update()
            points = camera_matrix * -scene.main_camera.T * -scene.main_camera.R * obj.transformed_vertices
            # perspective
            points = points[:2, :] / points[2, :]
            logger.info(f"rendering {name}")
            for point in points.T.tolist():
                x1 = int(point[0])
                y1 = int(point[1])
                logger.info(f"rendering {(x1,y1)}")
                sdlgfx.filledCircleColor(context.sdlrenderer, x1, y1, 3, sdlgfx_green)
        context.present()
        # self.draw_hud(hud)
        self.window.refresh()

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

