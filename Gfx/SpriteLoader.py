from Gfx.SpriteSheet import SpriteSheet
import pygame as pg
from Misc.FileIO import *
from Misc.Settings import *


class SpriteLoader:
    def __init__(self, game_obj):
        self.game = game_obj
        self.root_path = FILEPATHS["spritesheets"]
        self.sprites = {}
        self.tile_config = open_file(join(FILEPATHS["config"], "tile_config.json"))
        self.sprite_sets = open_file(join(FILEPATHS["config"], "spriteconfig.json"))
        self.load_sprites()

    def load_sprites(self):
        image_set = {}
        tile_index = 0
        for file in files_in_path(self.root_path):
            file_path = "{root}\\{file}".format(root=self.root_path, file=file)
            spritesheet, sprite_size = SpriteSheet(file_path), pg.image.load(file_path).get_rect().size

            current_image_set = {}

            colorkey = None

            for y in range(0, sprite_size[1], TILESIZE):
                for x in range(0, sprite_size[0], TILESIZE):
                    image_rect = (x, y, TILESIZE, TILESIZE)
                    if str(tile_index) in list(self.tile_config.keys()):
                        tile_config = self.tile_config[str(tile_index)]
                        if "colorkey" in list(tile_config.keys()):
                            ck = tile_config["colorkey"]
                            colorkey = (ck[0], ck[1], ck[2])

                    if colorkey is None:
                        current_image_set = {**current_image_set, tile_index: spritesheet.image_at(image_rect)}
                    else:
                        current_image_set = {**current_image_set,
                                             tile_index: spritesheet.image_at(image_rect, colorkey=colorkey)}

                    tile_index += 1
            image_set = {**image_set, **current_image_set}
        self.sprites = image_set

    def get_tile(self, tile_id=0):
        return self.sprites[int(tile_id)]

    def load_spriteset(self, object_id):
        for category in list(self.sprite_sets.keys()):
            if has_key(object_id, self.sprite_sets[category]):
                    return self.sprite_sets[category][object_id]
        return False