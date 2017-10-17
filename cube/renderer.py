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
    def __init__(self, width=800, height=600, f=2000, window_title="CUBE", delay_interval=10):
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
        self.context.clear(0)
        self.context.present()
        self.context.clear(0)

        self.delay_interval = delay_interval

    def screenshot(self):
        pass
        # can we do this?
        #  https://stackoverflow.com/questions/22315980/sdl2-c-taking-a-screenshot
        # SDL_Surface *sshot = SDL_CreateRGBSurface(0, w, h, 32, 0x00ff0000, 0x0000ff00, 0x000000ff, 0xff000000);
        # SDL_RenderReadPixels(renderer, NULL, SDL_PIXELFORMAT_ARGB8888, sshot->pixels, sshot->pitch);
        # SDL_SaveBMP(sshot, "screenshot.bmp");
        # SDL_FreeSurface(sshot);

    def draw_axes(self, scene, length=1):

        axes = np.matrix([
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [1, 1, 1, 1],
        ], dtype=np.float)

        axes[:3, :] *= length

        points = [tuple(x) for x in self.vertices_to_screen(scene, axes).T.A]

        if len(points) < 4:
            return

        # each axis is (color, endpoints)
        lines = (
            (0xff0000ff, points[0], points[1]),
            (0xff00ff00, points[0], points[2]),
            (0xffff0000, points[0], points[3]),
        )

        for color, p1, p2 in lines:
            sdlgfx.aalineColor(self.context.sdlrenderer, p1[0], p1[1], p2[0], p2[1], color)

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
        # if np.any(transformed_vertices[2, :] < 0):
        #     return
        points = camera_matrix * transformed_vertices

        # perspective
        points = points[:2, :] / points[2, :]

        points_int = points.astype(np.int32)
        return points_int

    def combine_vertices(self, vertices):
        pass

    def draw_points(self, renderer, points, color=0xff00ff00):
        circle = sdlgfx.filledCircleColor
        for x, y in points:
            circle(renderer, x, y, 2, color)

    def draw_edges(self, renderer, points, edges, color=0xff00ff00):
        line = sdlgfx.lineColor
        # line = sdlgfx.aalineColor
        for p1, p2 in edges:
            x1, y1 = points[p1]
            x2, y2 = points[p2]
            line(renderer, x1, y1, x2, y2, color)

    def render(self, hud, scene, clear=True, axes=False):

        self.frame += 1
        context = self.context
        if clear:
            context.clear(0)
        renderer = context.sdlrenderer

        vertices = []
        edges = []
        n_points = 0
        for name, obj in scene.objects.items():
            obj.update()
            obj_vertices = obj.transformed_vertices
            vertices.append(obj_vertices)
            # increment edge index
            obj_edges = [((edge[0]+n_points), (edge[1] + n_points)) for edge in obj.edges]
            edges.extend(obj_edges)
            n_points += obj_vertices.shape[1]

        vertices_matrix = np.hstack(vertices)
        points = self.vertices_to_screen(scene, vertices_matrix)

        points_list = points.T.tolist()
        self.draw_points(renderer, points_list)
        self.draw_edges(renderer, points_list, edges)

        if axes:
            self.draw_axes(scene)
        context.present()
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
            [f, 0, cx, 0],
            [0, -f, cy, 0],
            [0, 0, 1, 0]
        ], dtype=np.float64)

    def delay(self):
        sdl2.SDL_Delay(self.delay_interval)

    def quit(self):
        sdl2.ext.quit()

