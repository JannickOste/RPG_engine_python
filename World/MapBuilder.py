import pygame as py

from Entity.GameObject import GameObject
from Entity.GameTile import FloorTile
from Entity.Player import Player
from Misc.Settings import *
from Misc.FileIO import *
from World.MapHandler import MapHandler


class MapBuilder(MapHandler):
    def __init__(self, gameobj):
        super().__init__(gameobj)

    '''
        @func: spawn_objects()
        @desc: 
            * Will create all in game objects, like tiles, houses, player at level load.
    '''

    def load(self):
        self.get_map_configuration()

        self.spawn_floor_tiles()
        self.spawn_objects()

        # Spawn player
        for key in list(self.map_config["current_map"]["objects"].keys()):
            current_obj = self.map_config["current_map"]["objects"][key]
            if current_obj["object_id"] == "player":
                self.game.player = Player(self.game, current_obj["x"], current_obj["y"])

    def spawn_floor_tiles(self):
        # Loading required configuration.
        map_tiles = self.map_config["current_map"]["tiles"]
        x_rows, y_rows = self.map_config["current_map"]["x_rows"], self.map_config["current_map"]["y_rows"]

        # Loop through all rows and columns and creating correct tile.
        for y in range(0, y_rows-1):
            for x in range(0, x_rows-1):
                if map_tiles[y][x] != "":
                    FloorTile(self.game, x, y, int(map_tiles[y][x]))

    def spawn_objects(self):
        map_objects = {**self.map_config["current_map"]["objects"]}

        # Loop through all objects in current map's object file.
        for object_num in list(map_objects.keys()):
            # Foreach individual tile
            object_config, object_id = map_objects[object_num], map_objects[object_num]["object_id"]

            if object_id != "player":
                # Object identifier is object id and not a grouped tileset.
                if str(object_id).isdigit():
                    self.make_object(x=object_config["x"], y=object_config["y"], object_id=object_id)
                # Object identifier is grouped tile_set.
                elif self.game.sprite_handler.load_spriteset(object_id):
                    self.make_object(x=object_config["x"], y=object_config["y"],
                                     object_id=self.game.sprite_handler.load_spriteset(object_id))


