from Misc.FileIO import *

GAME_NAME = "Camelot RPG"

FILEPATHS = {
    "spritesheets" : "Lib\\SpriteSheets",
    "maps" : "Lib\\Maps",
    "config" : "Lib\\Cfg"
}

WINDOW_SIZE = (1024, 768)
TILESIZE = 32
ENABLE_GRID = True
FPS = 60


def load_configuration(config_name,  config_file):
    return open_file(join(FILEPATHS[config_name], config_file))

def has_key(key, search_dict):
    if key in list(search_dict.keys()):
        return True
    return False