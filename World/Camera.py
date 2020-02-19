import pygame as pg
from Misc.Settings import *



class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WINDOW_SIZE[0] / 2)
        y = -target.rect.y + int(WINDOW_SIZE[1] / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WINDOW_SIZE[0]), x)  # right
        y = max(-(self.height - WINDOW_SIZE[1]), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)