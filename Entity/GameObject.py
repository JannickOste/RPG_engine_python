from Gfx.SpriteTemplate import SpriteTemplate
from Misc.Settings import *


class GameObject(SpriteTemplate):
    def __init__(self, game, x, y, tile_id):
        self.game = game
        super().__init__(game, x, y, self.game.sprites["objects"], self.game.sprite_handler.get_tile(tile_id))

        self.x = x
        self.y = y
        self.walkable = False