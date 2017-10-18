import logging
import math

import numpy as np
import sdl2
import sdl2.ext
from sdl2 import sdlgfx

width=800
height=600
sdl2.ext.init()
window = sdl2.ext.Window('window_title', size=(width, height))
window.show()
# surface = window.get_surface()
context = sdl2.ext.Renderer(window)

sdlgfx_green = 0xFFFFFFFF  # 255 << 8

t=0
context.present()
context.present()
while True:
    # context.clear(0)
    # t += 1
    # r = int(20 * (math.sin(t/20) + 1))
    # print(r)
    # for i in range(0, 800, 20):
        # for j in range(0, 600, 20):
# 
            # sdlgfx.circleColor(context.sdlrenderer, i, j, r, sdlgfx_green)
    # renderer = surface
    points = (100, 100, 200, 200,
        100, 200, 200, 100,)
    count = 5
    context.draw_line( points )
    # sdl2.SDL_RenderDrawLines(renderer, points, count)
    sdl2.SDL_Delay(20)
    context.clear(0)


