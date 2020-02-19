from World.GameObject import GameObject


class FloorTile(GameObject):
    def __init__(self, game, x, y, tile_id, walkable=True):
        super().__init__(game, x, y, tile_id, walkable, group=game.sprites["tiles"])
        self.walkable = True