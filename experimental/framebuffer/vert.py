import random

import sdl2
import sdl2.ext
from sdl2 import sdlgfx


width=800
height=600

window = sdl2.ext.Window('window_title', size=(width, height))
window.show()

surface = window.get_surface()

pixels = sdl2.ext.pixels2d(surface)

while True:
    skip = random.randint(2,20)
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    color = (r << 16) + (g << 8) + b
    for i in range(0, width, skip):
        pixels[i:i+2,:] = color
    window.refresh()
    sdl2.SDL_Delay(5)
# sdl2.SDL_Delay(3000)
# sdl2.ext.quit()
