from Entity.GameObject import GameObject
from Misc.FileIO import *
from Misc.Settings import *


class MapHandler:
    def __init__(self, game):
        self.map_config = {"current_map"}
        self.game = game

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
        self.get_adjective()

    def is_teleport_tile(self, dest_x, dest_y):
        for object_id in list(self.map_config["current_map"]["objects"].keys()):
            current_obj = self.map_config["current_map"]["objects"][object_id]
            if has_key("teleport", current_obj):
                if current_obj["x"] == dest_x and current_obj["y"] == dest_y:
                        return True
        return False

    def get_adjective(self):
        pos_list = []
        for object_id in list(self.map_config["current_map"]["objects"].keys()):
            current_obj = self.map_config["current_map"]["objects"][object_id]
            if current_obj["object_id"] != "player":
                skip = False
                if has_key("walkable", current_obj):
                    skip = current_obj["walkable"]

                if not skip:
                    x, y = current_obj["x"], current_obj["y"]
                    x_is_list, y_is_list = isinstance(x, list), isinstance(y, list)
                    if isinstance(current_obj["object_id"], int) or str(current_obj["object_id"]).isdigit():
                        if x_is_list and not y_is_list:
                            for cur_x in range(x[0], x[1]):
                                pos_list.append([cur_x, y])
                        if y_is_list and not x_is_list:
                            for cur_y in range(y[0], y[1]):
                                pos_list.append([x, cur_y])
                        if not x_is_list and not y_is_list:
                            pos_list.append([x, y])
                    elif has_key(current_obj["object_id"], self.game.sprite_handler.sprite_sets):
                        set_info = self.game.sprite_handler.load_spriteset(current_obj["object_id"])
                        print(len(set_info))
                        if not y_is_list and not x_is_list:
                            for y_row in range(len(set_info)):
                                for x_row in range(0, len(set_info[y_row])):
                                    pos_list.append([x+x_row, y+y_row])
                        elif y_is_list and not x_is_list:
                            offset_list = [y for y in range(y[0], y[1], len(set_info))]
                            for index in range(len(offset_list)):
                                for y_row in range(len(set_info)):
                                    for x_row in range(0, len(set_info[y_row])):
                                        pos_list.append([x+x_row, offset_list[index]+y_row])
                        elif x_is_list and not y_is_list:
                            offset_list = [x for x in range(x[0], x[1], len(set_info))]
                            for index in range(len(offset_list)):
                                for y_row in range(len(set_info)):
                                    for x_row in range(0, len(set_info[y_row])):
                                        pos_list.append([offset_list[index]+x_row, y+y_row])
        self.map_config["current_map"]["adjective"] = pos_list

    def path_walkable(self, dest_x, dest_y):
        adjective_paths = self.map_config["current_map"]["adjective"]
        for path in adjective_paths:
            if dest_x == path[0]*TILESIZE and dest_y == path[1]*TILESIZE:
                return False
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
                range_list = [x for x in range(x[0], x[1], set_size[0])] if isinstance(x, list) else [y for y in range(y[0], y[1], set_size[1])]
                for index in range(0, len(range_list)-1):
                    for y_row in range(0, len(object_id)):
                        for x_row in range(len(object_id[y_row])):
                            if isinstance(x, list):
                                self.make_object(x=range_list[index]+x_row, y=y+y_row, object_id=object_id[y_row][x_row])
                            else:
                                self.make_object(x=x+x_row, y=y_row+range_list[index], object_id=object_id[y_row][x_row])

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