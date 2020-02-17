from Entity.GameObject import GameObject
from Misc.FileIO import *
from Misc.Settings import *


class MapHandler:
    def __init__(self):
        self.x_rows, self.y_rows = 0, 0
        self.map_data = []
        self.map_objects = []
        self.sprite_sets = {}
        self.map_config = {}

    def get_map_configuration(self):
        current_map_values = {
            'tiles': [line.strip("\n").split(" ") for line in open_file(join(FILEPATHS["maps"], self.game.gamestate + ".cfg"))],
            'objects': open_file(join(FILEPATHS["maps"], self.game.gamestate + "_objects.json"))
        }

        global_map_values = {
            "tile_configuration" :  load_configuration("config", "tile_config.json")
        }

        self.map_config = {
            "current_map":{
                **current_map_values,
                **{
                    "y_rows" : len(current_map_values["tiles"]),
                    "x_rows" : len(current_map_values["tiles"][0])
                }
            },
            "global" : {
                **global_map_values
            }
        }

    def is_teleport_tile(self, dest_x, dest_y):
        for object_id in list(self.map_config["current_map"]["objects"].keys()):
            current_obj = self.map_config["current_map"]["objects"][object_id]
            if has_key("teleport", current_obj):
                if current_obj["x"] == dest_x and current_obj["y"] == dest_y:
                        return True
        return False

    def path_walkable(self, dest_x, dest_y):
        for object_id in list(self.map_config["current_map"]["objects"].keys()):
            current_obj = self.map_config["current_map"]["objects"][object_id]
            if current_obj["x"] == dest_x and current_obj["y"] == dest_y:
                if not has_key("walkable", current_obj) and current_obj["object_id"] != "player":
                    return False
                else:
                    return self.map_objects[object_id]["walkable"]
        return True

    def get_teleport_location(self, dest_x, dest_y):
        for object_id in list(self.map_config["current_map"]["objects"].keys()):
            current_obj = self.map_config["current_map"]["objects"][object_id]

            if has_key("teleport", self.map_objects[object_id]):
                if self.map_objects[object_id]["x"] == dest_x and self.map_objects[object_id]["y"] == dest_y:
                    return self.map_objects[object_id]["teleport"]
        return False


    def make_object(self, x=0, y=0, object_id=None):
        def fixed_draw():
            # Make single object at fixed position.
            if isinstance(object_id, int):
                GameObject(self.game, x, y, object_id)
            elif isinstance(object_id, list):
                for set_y in range(len(object_id)):
                    for set_x in range(len(object_id[0])):
                        self.make_object(x=x+set_x, y=y+set_y, object_id=object_id[set_y][set_x])

        def linair_draw():
            # Make multiple single object in horizontal/vertical line
            if isinstance(object_id, int):
                range_list = [x for x in range(x[0], x[1])] if isinstance(x, list) else [y for y in range(y[0], y[1])]
                for list_index, offset in enumerate(range_list):
                    if isinstance(x, list):
                        self.make_object(x=range_list[list_index], y=y, object_id=object_id)
                    else:
                        self.make_object(x=x, y=range_list[list_index], object_id=object_id)
            elif isinstance(object_id, list):
                set_size = max([len(row) for row in object_id]), len(object_id)
                range_list = [x for x in range(x[0], x[1], set_size[0])] if isinstance(x, list) else [y for y in range(y[0], y[1], set_size[0])]

                for list_index, offset in enumerate(range_list):
                    for y_row in range(0, len(object_id)):
                        for x_row in (0, len(object_id[y_row])-1):
                            if isinstance(x, list):
                                self.make_object(x=range_list[list_index]+x_row, y=y+y_row, object_id=object_id[y_row][x_row])
                            else:
                                self.make_object(x=x+x_row, y=y_row+range_list[list_index], object_id=object_id[y_row][x_row])
        def rectangulair_draw():
            if isinstance(object_id, int):
                for tile_y in range(y[0], y[1]):
                    for tile_x in range(x[0], x[1]):
                        self.make_object(x=tile_x, y=tile_y, object_id=object_id)
            else:
                print("hi")

        if all([not isinstance(x, list), not isinstance(y, list)]):
            fixed_draw()
        elif any([isinstance(x, list) and not isinstance(y, list), isinstance(y, list) and not isinstance(x, list)]):
            linair_draw()
        elif all([isinstance(x, list), isinstance(y, list)]):
            rectangulair_draw()