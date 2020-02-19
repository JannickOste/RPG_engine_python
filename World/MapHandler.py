import itertools

from Entity.Entity import Entity
from Entity.Player import Player
from World.GameObject import GameObject

from Misc.Settings import *


class MapHandler:
    def __init__(self, game):
        self.map_config = {"current_map"}
        self.game = game
        self.map_buffer = {}

    def is_teleport_tile(self, dest_x, dest_y):
        for object_id in list(self.map_config["current_map"]["objects"].keys()):
            current_obj = self.map_config["current_map"]["objects"][object_id]
            if has_key("teleport", current_obj):
                if current_obj["x"] == dest_x and current_obj["y"] == dest_y:
                    return True
        return False

    def is_map_changer(self, dest_x, dest_y):
        for object_id in list(self.map_config["current_map"]["objects"].keys()):
            current_obj = self.map_config["current_map"]["objects"][object_id]
            if 'gamestate' in list_keys(current_obj):
                if current_obj["x"] == dest_x//TILESIZE and current_obj["y"] == dest_y//TILESIZE:
                    self.game.gamestate = current_obj["gamestate"]
                    return True
        return False

    def new_map_name(self, dest_x, dest_y):
        for object_id in list(self.map_config["current_map"]["objects"].keys()):
            current_obj = self.map_config["current_map"]["objects"][object_id]
            if 'gamestate' in list_keys(current_obj):
                if current_obj["x"] == dest_x//TILESIZE and current_obj["y"] == dest_y//TILESIZE:
                    return current_obj["gamestate"]
        return False

    def spawn_entitys(self):
        for entity in self.map_config["current_map"]["entitys"]:
            current_entity = self.map_config["current_map"]["entitys"][entity]

            if entity == "player":
                self.game.entity_handler.set_entity(current_entity["x"], current_entity["y"], current_entity["id"], player=True)
            else:
                self.game.entity_handler.set_entity(current_entity["x"], current_entity["y"], current_entity["id"])



    #  Check or destination path is actually accessible
    def path_walkable(self, entity):
        sprite_lib = self.game.sprites
        for game_object in itertools.chain(sprite_lib["objects"], sprite_lib["tiles"]):
            if all([entity.dest_x//TILESIZE == game_object.x, entity.dest_y//TILESIZE == game_object.y]) \
                    or any([isinstance(entity.rect.x, float), isinstance(entity.rect.y, float)]):
                if not game_object.walkable:
                    print(entity.rect.y, entity.dest_y)
                    return False
        return True


    def get_teleport_location(self, dest_x, dest_y):
        for object_id in list(self.map_config["current_map"]["objects"].keys()):
            current_obj = self.map_config["current_map"]["objects"][object_id]

            if has_key("teleport", self.map_objects[object_id]):
                if current_obj["x"] == dest_x and current_obj["y"] == dest_y:
                    return current_obj["teleport"]
        return False

    def make_object(self, walkable, x=0, y=0, object_id=None):
        def fixed_draw():
            # Make single object at fixed position.
            if isinstance(object_id, int):
                GameObject(self.game, x, y, object_id, walkable=walkable)
            elif isinstance(object_id, list):
                if not isinstance(object_id[0], int):
                    for set_y in range(len(object_id)):
                        for set_x in range(len(object_id[0])):
                            self.make_object(walkable, x=x + set_x, y=y + set_y, object_id=object_id[set_y][set_x])
                else:
                    for offset in range(len(object_id)):
                        if isinstance(x, list):
                            self.make_object(walkable, x=x, y=y + offset, object_id=object_id[offset])
                        else:
                            self.make_object(walkable, x=x + offset, y=y, object_id=object_id[offset])

        def linair_draw():
            # Make multiple single object in horizontal/vertical line
            if isinstance(object_id, int):
                range1, range2 = (x[0], x[1]) if isinstance(x, list) else (y[0], y[1])

                for offset in range(range1, range2+1):
                    if isinstance(x, list):
                        self.make_object(walkable, x=offset, y=y, object_id=object_id)
                    else:
                        self.make_object(walkable, x=x, y=offset, object_id=object_id)
            elif isinstance(object_id, list):
                set_size = max([len(row) for row in object_id]), len(object_id)
                range_list = [x for x in range(x[0], x[1], set_size[0])] if isinstance(x, list) else [y for y in
                                                                                                      range(y[0], y[1],
                                                                                                            set_size[
                                                                                                                1])]
                for index in range(0, len(range_list) - 1):
                    for y_row in range(0, len(object_id)):
                        for x_row in range(len(object_id[y_row])):
                            if isinstance(x, list):
                                self.make_object(walkable, x=range_list[index] + x_row, y=y + y_row,
                                                 object_id=object_id[y_row][x_row])
                            else:
                                self.make_object(walkable, x=x + x_row, y=y_row + range_list[index],
                                                 object_id=object_id[y_row][x_row])

        def rectangulair_draw():
            if isinstance(object_id, int):
                for tile_y in range(y[0], y[1]+1):
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

    def object_at(self, x, y):
        for size in self.map_config["current_map"]["adjective"]:
            if x == size[0] and y == size[1]:
                return True
        return False
