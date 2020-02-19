from World.FloorTile import FloorTile
from World.MapHandler import MapHandler
from  Misc.Settings import *
import pygame as pg

class MapBuilder(MapHandler):
    def __init__(self, gameobj):
        super().__init__(gameobj)
        self.map_data = open_file(join(FILEPATHS["config"], "maps.json"))
        self.all_map_objects = open_file(join(FILEPATHS["config"], "map_objects.json"))
        self.all_map_entitys = open_file(join(FILEPATHS["config"], "entitys.json"))

    '''
        @func: spawn_objects()
        @desc: 
            * Will create all in game objects, like tiles, houses, player at level load.
    '''

    def load(self, map_config):
        self.game.sprites = {
            "tiles": pg.sprite.Group(),
            "objects": pg.sprite.Group(),
            "player": pg.sprite.Group(),
            "npcs": pg.sprite.Group()
        }
        self.get_map_configuration(map_config)
        print(self.all_map_objects)
        self.spawn_floor_tiles()
        self.spawn_objects()
        self.spawn_entitys()


    def get_map_configuration(self, map_config):
        tiles_list = []
        for map_name in list(self.map_data.keys()):
            if map_config == map_name:
                for y in self.map_data[map_name]:
                    list_row = []
                    for x in self.map_data[map_name]:
                        list_row.append(x)
                    tiles_list.append(list_row)
        print(self.all_map_entitys)
        current_map_values = {
                'tiles': tiles_list,
                'objects': self.all_map_objects[map_config],
                "entitys": self.all_map_entitys[map_config]
        }

        global_map_values = {
            "tile_configuration": load_configuration("config", "tile_config.json")
        }

        self.map_config = {
            "current_map": {
                **current_map_values,
                **{
                    "y_rows": len(current_map_values["tiles"]),
                    "x_rows": len(current_map_values["tiles"][0])
                }
            },
            "global": {
                **global_map_values
            }
        }

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
            walkable = object_config["walkable"] if "walkable" in list(object_config.keys()) else False

            # Object identifier is object id and not a grouped tileset.
            if object_id == "player" or str(object_id).startswith("npc_"):
                pass
            elif str(object_id).isdigit():
                self.make_object(walkable, x=object_config["x"], y=object_config["y"], object_id=object_id)
            # Object identifier is grouped tile_set.
            elif self.game.sprite_handler.load_spriteset(object_id):
                self.make_object(walkable, x=object_config["x"], y=object_config["y"],
                                object_id=self.game.sprite_handler.load_spriteset(object_id))



