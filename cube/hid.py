""" hid.py -- Human Interface Devices """

import sdl2

def drive_obj(obj):

    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.scancode == sdl2.SDL_SCANCODE_DOWN:
                obj.rotation.y += .1
            elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_UP:
                obj.rotation.y -= .1
            elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_LEFT:
                obj.rotation.x += .1
            elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_RIGHT:
                obj.rotation.x -= .1
            elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_S:
                obj.position.z -= 5
            elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_W:
                obj.position.z += 5
            elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_Q:
                raise Exception("quit")
        if event.type == sdl2.SDL_QUIT:
            raise Exception("quit")