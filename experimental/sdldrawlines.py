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
context = sdl2.ext.Renderer(window)

sdlgfx_green = 0xFFFFFFFF  # 255 << 8

t=0
while True:
    context.clear(0)
    t += 1
    r = int(20 * (math.sin(t/20) + 1))
    print(r)
    # for i in range(0, 800, 20):
        # for j in range(0, 600, 20):
# 
            # sdlgfx.circleColor(context.sdlrenderer, i, j, r, sdlgfx_green)
    lines = (0, 0, 100, 100, 200, 100, 900, 400)
    color = sdl2.ext.Color(r=0, g=255, b=0, a=255)
    context.draw_line(lines, color)
    context.present()
    sdl2.SDL_Delay(20)


