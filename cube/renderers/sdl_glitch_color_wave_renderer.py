import logging
import math
import random

import numpy as np
import sdl2
import sdl2.ext
from sdl2 import sdlgfx


logger = logging.getLogger(__name__)


class Renderer(): pass


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
        # pass
        # can we do this?
        #  https://stackoverflow.com/questions/22315980/sdl2-c-taking-a-screenshot
        # SDL_Surface *sshot = SDL_CreateRGBSurface(0, w, h, 32, 0x00ff0000, 0x0000ff00, 0x000000ff, 0xff000000);
        # SDL_RenderReadPixels(renderer, NULL, SDL_PIXELFORMAT_ARGB8888, sshot->pixels, sshot->pitch);
        # SDL_SaveBMP(sshot, "screenshot.bmp");
        # SDL_FreeSurface(sshot);
        sdl2.SDL_SaveBMP(self.window.get_surface(), "/tmp/foo.bmp")

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

        points_int = points.round().astype(np.int32)
        return points_int

    def combine_vertices(self, vertices):
        pass

    def draw_vertices(self, renderer, points, color=0xff00ff00):
        circle = sdlgfx.aacircleColor
        # circle = sdlgfx.filledCircleColor
        for x, y in points:
            circle(renderer, x, y, 2, color)

    def draw_edges(self, renderer, points, edges, color=0xff00ff00):
        # line = sdlgfx.lineColor
        line = sdlgfx.aalineColor
        for p1, p2 in edges:
            x1, y1 = points[p1]
            x2, y2 = points[p2]
            line(renderer, x1, y1, x2, y2, color)

    def draw_polys(self, renderer, points, polys, color=0xff00ff00):
        original_color = color


        line = sdlgfx.lineColor
        # line = sdlgfx.aalineColor
        for p1, p2, p3 in polys:

            global toggle
            toggle += 1
            if (toggle // 10000) % 2 == 0:
                color = 0xff000000
                r = 0 # self.frame % 255
                g = 0 # frame % 255 # random.randint(0,255)
                b = self.frame % 255 # random.randint(0,255)
                color += (r << 16)
                color += (g << 8)
                color += b
            else:
                color = 0xfffccffc # original_color

            x1, y1 = points[p1]
            x2, y2 = points[p2]
            line(renderer, x1, y1, x2, y2, color)

            x1, y1 = points[p1]
            x2, y2 = points[p3]
            line(renderer, x1, y1, x2, y2, color)

            x1, y1 = points[p2]
            x2, y2 = points[p3]
            line(renderer, x1, y1, x2, y2, color)

            # slow
            # lines = (*points[p1], *points[p2], *points[p3])
            # color = sdl2.ext.Color(r=255, g=255, b=0, a=255)
            # self.context.draw_line(lines, color)

    def render(self, hud, scene, clear=True, axes=False, draw_vertices=True, draw_polys=True):

        self.frame += 1
        context = self.context
        if clear:
            context.clear(0)
        renderer = context.sdlrenderer

        vertices = []
        edges = []
        polys = []
        n_points = 0
        for name, obj in scene.objects.items():
            obj.update()
            obj_vertices = obj.transformed_vertices
            vertices.append(obj_vertices)
            # increment edge index
            obj_edges = [((edge[0]+n_points), (edge[1] + n_points)) for edge in obj.edges]
            edges.extend(obj_edges)

            obj_polys = [((face[0]+n_points), (face[1] + n_points), (face[2] + n_points)) for face in obj.polys]
            polys.extend(obj_polys)

            n_points += obj_vertices.shape[1]

        vertices_matrix = np.hstack(vertices)
        points = self.vertices_to_screen(scene, vertices_matrix)

        points_list = points.T.tolist()
        if draw_vertices:
            self.draw_vertices(renderer, points_list)
        self.draw_edges(renderer, points_list, edges)
        if draw_polys:
            self.draw_polys(renderer, points_list, polys)

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

