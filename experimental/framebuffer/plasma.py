import random

import numpy as np
import sdl2
import sdl2.ext
from sdl2 import sdlgfx


w = 1200
h = 800

window = sdl2.ext.Window('window_title', size=(w, h))
window.show()

surface = window.get_surface()

pixels = sdl2.ext.pixels2d(surface).T

ix,iy = np.meshgrid(np.arange(0,w), np.arange(0,h))

ix = ix.astype(np.float32)
iy = iy.astype(np.float32)

def noise_function(x, y, phase=0):
    # hack for now
    # yy = y[:,0].reshape(h,1)
    # yy *= w
    return x + y

noise = noise_function(ix / 100, iy / 100)

freq = 1
wx = 1/50
wy = 1/53
while True:
    # noise += 0.01
    wx += (random.random()-0.5) / 2000
    wy += (random.random()-0.5) / 3000
    # r = random.randint(0,255)
    # g = random.randint(0,255)
    # b = random.randint(0,255)
    # color = (r << 16) + (g << 8) + b
    # plasma is sin(f(x,y) * freq))
    x = (np.sin(wx * ix + wx) + np.sin(wy*iy +wy) + 2) / 4
    # x = np.linalg.norm((np.sin(ix) + np.sin(iy) + 2))
    r = g = b = (x * 127).astype(np.uint8)
    # r = g = b = 127 * (np.sin(freq*noise) + 1)
    # g = 127 * (np.sin(freq*noise) + 1)
    # b = 127 * (np.sin(freq*noise) + 1)
    pixels[:,:] = r * 65536 + g * 256 + b  # emulate bitshifting
    pixels[:,:] = g * 256
    window.refresh()
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.scancode == 81:  # down arrow
                freq += 0.025
            elif event.key.keysym.scancode == 82:  # up arrow
                freq -= 0.025
        elif event.type == sdl2.SDL_QUIT:
            break
    sdl2.SDL_Delay(10)
# sdl2.SDL_Delay(3000)
# sdl2.ext.quit()
