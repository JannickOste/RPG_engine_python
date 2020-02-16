from GameHandler import GameHandler
from Misc.Settings import *
import pygame as pg

"""
    @Project_name: PyTile Engine.
    @Author: Oste Jannick.
    @ Start date: 15/02/2020
    @Class: Game()
"""


class Game(GameHandler):
    '''
        @func: __init__()
        @desc: Instantiates gamehandler file, containing handlers and global game variables.
    '''

    def __init__(self):
        super().__init__()

    '''
        @func: start_game()
        @desc: Actual game loop actions foreach game tick that passes. 
    '''

    def start_game(self):
        self.init_components(self)
        new_update = pg.time.get_ticks() + 60
        while self.running:
            # Check for events -> Update values -> render updates.
            if pg.time.get_ticks() > new_update:
                self.event_handler.listen()
                self.update()
                self.render()
                new_update = pg.time.get_ticks() + 60


g = Game()
g.start_game()
