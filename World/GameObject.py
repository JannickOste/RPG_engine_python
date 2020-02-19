from Gfx.SpriteTemplate import SpriteTemplate

"""
    @Class: GameObject()
    - Object template for all actual objects on map.
"""


class GameObject(SpriteTemplate):
    def __init__(self, game, x, y, tile_id, walkable=False, image=None, group=None):
        self.game = game
        self.tile_id = tile_id
        group = self.game.sprites["objects"] if group is None else group
        image = image if image is not None else self.game.sprite_handler.get_tile(int(tile_id))

        super().__init__(game, x, y, group, image)

        self.x = x
        self.y = y
        self.walkable = walkable
