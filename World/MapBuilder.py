import pygame as py

from Entity.GameObject import GameObject
from Entity.GameTile import FloorTile
from Entity.Player import Player
from Misc.FileIO import *
from Misc.Settings import *


class MapBuilder:
    def __init__(self, gameobj):
        self.game = gameobj
        self.x_rows, self.y_rows = 0, 0
        self.map_data = []
        self.map_objects = []
        self.sprite_sets = {}

    '''
        @func: spawn_objects()
        @desc: 
            * Will create all in game objects, like tiles, houses, player at level load.
    '''

    def load(self):
        self.map_data =  [line.strip("\n").split(" ") for line in open_file(join(FILEPATHS["maps"], self.game.gamestate+".cfg"))]
        self.map_objects = open_file(join(FILEPATHS["maps"], self.game.gamestate+"_objects.json"))
        self.sprite_sets = open_file(join(FILEPATHS["config"], "spritesets.json"))
        self.x_rows = len(self.map_data[0])
        self.y_rows = len(self.map_data)

        self.spawn_floor_tiles()
        self.spawn_objects()

        for key in list(self.map_objects.keys()):
            if self.map_objects[key]["object_id"] == "player":
                self.game.player = Player(self.game, self.map_objects[key]["x"], self.map_objects[key]["y"])

    def spawn_floor_tiles(self):
        for y in range(0, self.y_rows - 1):
            for x in range(0, self.x_rows - 1):
                if self.map_data[y][x] != "":
                    FloorTile(self.game, x, y, int(self.map_data[y][x]))

    def spawn_objects(self):
        # Spawn objects on top of tiles.

        for key in list(self.map_objects.keys()):
            object_data = self.map_objects[key]
            # If object id has been found in spritesets.
            if object_data["object_id"] in list(self.sprite_sets.keys()):
                set_tiles = self.sprite_sets[object_data["object_id"]]

                for y in range(len(set_tiles)):
                    for x in range(len(set_tiles[y])):
                        if not isinstance(object_data["x"], list) and not isinstance(object_data["y"], list):
                            GameObject(self.game, x + object_data["x"], y + object_data["y"], set_tiles[y][x])

            # If object is not found in spritesets and is not player.
            elif object_data["object_id"] != "player":
                GameObject(self, object_data["x"], object_data["y"], object_data["object_id"])
