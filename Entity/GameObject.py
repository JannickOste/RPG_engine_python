from Gfx.SpriteTemplate import SpriteTemplate
from Misc.Settings import *


class GameObject(SpriteTemplate):
    def __init__(self, game, x, y, tile_id, image=None):
        self.game = game
        image = image if image is not None else self.game.sprite_handler.get_tile(int(tile_id))

        super().__init__(game, x, y, self.game.sprites["objects"], image)

        self.x = x
        self.y = y
        self.walkable = False