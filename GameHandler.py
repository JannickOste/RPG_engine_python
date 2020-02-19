# Import interpeter packets.
import pygame as pg

from Gfx.SpriteLoader import SpriteLoader
from World.MapBuilder import MapBuilder
from EventHandler import EventHandler
from Entity.EntityHandler import EntityHandler

from World.Camera import Camera
from Misc.Settings import *

'''
    @Class: GameHandler()
    @Creation date: 15/02/2020
'''


class GameHandler:
    '''
        @func: __init__()
        @desc: Gamehandlers
            * initiate all global objects to avoid errors and for easy access.
    '''

    def __init__(self):
        self.running = False

        self.window, self.gamestate, self.clock = None, "", None
        self.event_handler, self.sprite_handler, self.game_render, self.entity_handler = None, None, None, None
        self.map_handler = None
        self.camera, self.map_handler = None, None

        self.sprites = {}

        self.player = None
        self.npcs = []
        self.entitys_set = False

    '''
        @func: init_components(game_obj)
        @desc: 
            * Instantiate all predefined initiated variables before running game loop.
    '''

    def init_components(self, game_obj):
        # Game Instantiation.
        pg.init()
        pg.display.set_caption(GAME_NAME)

        # Game Globals
        self.running = True
        self.gamestate = "calleas"
        self.clock = pg.time.Clock()
        self.window = pg.display.set_mode(WINDOW_SIZE)
        self.delta = self.clock.tick(FPS) / 1000

        # Game Handlers
        self.sprite_handler = SpriteLoader(game_obj)

        self.entity_handler = EntityHandler(game_obj)
        self.map_handler = MapBuilder(game_obj)
        self.map_handler.load(self.gamestate)
        self.event_handler = EventHandler(game_obj)

        self.camera = Camera(self.map_handler.map_config["current_map"]["x_rows"] * TILESIZE,
                             self.map_handler.map_config["current_map"]["y_rows"] * TILESIZE)

    '''
        @func: render()
        @desc: 
            * The render function is where all sprites will be drawn on screen. 
    '''

    def render(self):
        def draw_grid():
            for x in range(0, WINDOW_SIZE[0] + TILESIZE, TILESIZE):
                for y in range(0, WINDOW_SIZE[1] + TILESIZE, TILESIZE):
                    grid_color = (140, 140, 140)
                    pg.draw.line(self.window, grid_color, (TILESIZE - x, y), (x, y))
                    pg.draw.line(self.window, grid_color, (x, TILESIZE - y), (x, y))

        def draw_objects():
            for tile_group in list(self.sprites.keys()):
                for tile in self.sprites[tile_group]:
                    image = tile.image if tile_group != "player" else tile.get_walk_image(self.player)
                    self.window.blit(image, self.camera.apply(tile))

        draw_objects()

        if ENABLE_GRID:
            draw_grid()

        pg.display.update()
        pg.display.flip()

    '''
        @func: update()
        @desc: 
            * All game sprites, values, etc... will be updated here.
    '''

    def update(self):
        for sprite_group in ["objects", "tiles"]:
            self.sprites[sprite_group].update()

        self.entity_handler.update()

        self.camera.update(self.player)
