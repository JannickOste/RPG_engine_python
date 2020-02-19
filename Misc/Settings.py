from Misc.FileIO import *

from datetime import datetime, timedelta
from random import choice

GAME_NAME = "Camelot RPG"

FILEPATHS = {
    "spritesheets" : "Lib\\SpriteSheets",
    "maps" : "Lib\\Maps",
    "config" : "Lib\\Cfg"
}

WINDOW_SIZE = (1024, 768)
TILESIZE = 32
ENABLE_GRID = False
FPS = 60
PLAYER_SPEED = 3.4

def load_configuration(config_name,  config_file):
    return open_file(join(FILEPATHS[config_name], config_file))

def has_key(key, search_dict):
    if key in list(search_dict.keys()):
        return True
    return False

def current_time():
    return datetime.now().strftime("%H:%M:%S")

def delta_time(seconds=0):
    new_time = datetime.now()+timedelta(seconds=seconds)
    return new_time.strftime("%H:%M:%S")

def random_next_time():
    range_set = [x for x in range(15, 60)]
    return delta_time(choice(range_set))

def list_keys(dic):
    return list(dic.keys())