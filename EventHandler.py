import pygame as pg

from Misc.Settings import has_key

"""
    # @Class: EventHandler()
    - Handeling for all user input events. 
    
    @!todo: 
    - Add support for switchable user keys from options interface.
    - Add controller functionality.
"""


class EventHandler:
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
            if has_key("unicode", event.__dict__):
                event = event.__dict__
                if any([event["unicode"] == "q", event["unicode"] == "Q"]):
                    self.game.player.move(x=-1)
                if any([event["unicode"] == "d", event["unicode"] == "D"]):
                    self.game.player.move(x=1)
                if any([event["unicode"] == "z", event["unicode"] == "Z"]):
                    self.game.player.move(y=-1)
                if any([event["unicode"] == "s", event["unicode"] == "S"]):
                    self.game.player.move(y=1)


    def keyboard_events(self):
        keys = pg.key.get_pressed()
        keyboard_type = "azerty"
        key_dict = {
            "a" : keys[pg.K_a],
            "b" : keys[pg.K_b], "c" : keys[pg.K_c], "d" : keys[pg.K_d], "e" : keys[pg.K_e], "f" : keys[pg.K_f],
            "g" : keys[pg.K_g], "h" : keys[pg.K_h], "i" : keys[pg.K_i], "j" : keys[pg.K_j],
            "k" : keys[pg.K_k], "l" : keys[pg.K_l], "m" : keys[pg.K_m],
            "n" : keys[pg.K_n],  "o" : keys[pg.K_o], "p" : keys[pg.K_p],
            "q" : keys[pg.K_q] if keyboard_type=="qwerty" else keys[pg.K_a],
            "r" : keys[pg.K_r], "s" : keys[pg.K_s], "t" : keys[pg.K_t],
            "u" : keys[pg.K_u], "v" : keys[pg.K_v], "w" : keys[pg.K_w], "x" : keys[pg.K_x], "y" : keys[pg.K_y],
            "z" : keys[pg.K_z] ,
            "left" : keys[pg.K_LEFT]
        }

        if not self.game.player.moving:
            if key_dict["left"] or key_dict["q"]:
                self.game.player.move(x=-1)
            if keys[pg.K_RIGHT] or key_dict["d"]:
                self.game.player.move(x=1)
            if keys[pg.K_UP] or key_dict["z"]:
                self.game.player.move(y=-1)
            if keys[pg.K_DOWN] or key_dict["s"]:
                self.game.player.move(y=1)

            if keys[pg.K_v]:
                self.game.player.running = True
            else:
                self.game.player.running = False
