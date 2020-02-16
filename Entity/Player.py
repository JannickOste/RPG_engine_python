from Gfx.SpriteTemplate import SpriteTemplate
from Misc.Settings import *


class Player(SpriteTemplate):
    def __init__(self, game, x, y):
        self.game = game
        super().__init__(game, x, y, self.game.sprites["player"], self.game.sprite_handler.get_tile(1065))
        self.direction = "down"
        self.x = x
        self.y = y

    def move(self, dest_x=0, dest_y=0):
        if not self.object_walkable(dest_x, dest_y):
            self.x += dest_x
            self.y += dest_y

    def object_walkable(self, dest_x, dest_y):
        for obj in self.game.sprites["objects"]:
            if self.x + dest_x == obj.x and self.y + dest_y == obj.y:
                if not obj.walkable:
                    return True
        return False