import pygame as pg
from Misc.Settings import *


class EventHandler(object):
    def __init__(self, game_obj):
        self.game = game_obj

    def listen(self):
        self.mouse_events()
        self.keyboard_events()

    def mouse_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                self.game.running = False

    def keyboard_events(self):
        keys = pg.key.get_pressed()

        if not self.game.player.moving:
            if keys[pg.K_LEFT] or keys[pg.K_q]:
                self.game.player.move(x=-1)
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.game.player.move(x=1)
            if keys[pg.K_UP] or keys[pg.K_z]:
                self.game.player.move(y=-1)
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.game.player.move(y=1)
