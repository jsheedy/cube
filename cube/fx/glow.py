import sdl2

from .fx import FX


class GlowFX(FX):

    def render(self, renderer):
        surface = renderer.window.get_surface()
        pixels = sdl2.ext.pixels3d(surface)
        pixels += 100