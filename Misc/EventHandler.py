import pygame as pg


class EventHandler(object):
    def __init__(self, game_obj):
        self.game = game_obj

    def listen(self):
        self.mouse_events()
        self.keyboard_events()

    def keyboard_events(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_UP]:
            self.game.player.move(dest_y=-1)
        if keys[pg.K_LEFT]:
            self.game.player.move(dest_x=-1)
        if keys[pg.K_DOWN]:
            self.game.player.move(dest_y=1)
        if keys[pg.K_RIGHT]:
            self.game.player.move(dest_x=1)

    def mouse_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                self.game.running = False
