import pygame as pg

from Misc.Settings import *


# Default wrapper for sprite template.
class SpriteTemplate(pg.sprite.Sprite):
    def __init__(self, game, x, y, groups, image):
        self.groups = groups
        pg.sprite.Sprite.__init__(self, groups)

        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def get_pos(self, raw=False):
        if raw:
            return self.rect.x, self.rect.y
        else:
            return self.rect.x//TILESIZE, self.rect.y//TILESIZE

    def set_pos(self, x=None, y=None):
        if x is not None:
            self.rect.x = x
        if y is not None:
            self.rect.y = y
