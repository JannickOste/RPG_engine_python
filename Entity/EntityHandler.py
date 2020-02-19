from random import choice

from Entity.Entity import Entity
from Entity.Player import Player
from Misc.Settings import TILESIZE


class EntityHandler:
    def __init__(self, game):
        self.game = game
        self.npc_update_count = 0

    def set_entity(self, x, y, id, player=False):
        if player:
            print(self.game.player)
            self.game.player = Player(self.game, x, y, id)
        else:
            self.game.npcs.append(Entity(self.game, x, y, id))

    def update(self):
        self.game.player.update()

        for entity in self.game.npcs:
            entity.update()

