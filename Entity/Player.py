from Gfx.SpriteTemplate import SpriteTemplate
from Misc.Settings import *
import pygame as pg

class Player(SpriteTemplate):
    def __init__(self, game, x, y):
        self.game = game
        super().__init__(game, x, y, self.game.sprites["player"], self.game.sprite_handler.get_tile(1065))
        self.direction = "down"
        self.moving = False

        self.vel = pg.math.Vector2(0, 0)
        self.vx, self.vy = 0, 0
        self.dest_x, self.dest_y = 0, 0
        self.orig_x, self.orig_y = 0, 0

        self.player_speed = 3

    def get_pos(self):
        for sprite_obj in self.game.sprites["player"]:
            return sprite_obj.x, sprite_obj.y


    def move(self, x=0, y=0):
        if not self.moving and any([x>0, x<0]) or any([y>0, y<0]):
            self.vx, self.vy = 0, 0
            self.direction = "left" if 0 > x else "right" if x > 0 else "down" if y > 0 else "up"

            self.orig_x = self.rect.x
            self.orig_y = self.rect.y
            self.dest_x = self.orig_x-TILESIZE*abs(x) if x < 0 else self.orig_x+(TILESIZE*x) if x > 0 else self.orig_x
            self.dest_y = self.orig_y-TILESIZE*abs(y) if y < 0 else self.orig_y+(TILESIZE*y) if y > 0 else self.orig_y
            if self.path_walkable():
                self.moving = True
        else:
            self.move_animation()
            if self.direction == "up":
                    reset = True if self.rect.y < self.dest_y else False
            elif self.direction == "down":
                    reset = True if self.rect.y > self.dest_y else False
            elif self.direction == "left":
                    reset = True if self.rect.x < self.dest_x else False
            elif self.direction == "right":
                    reset = True if self.rect.x > self.dest_x else False
            if reset:
                self.reset_player()
                self.moving = False

    def move_animation(self):
        if self.direction == "up":
            self.rect.y += -TILESIZE//self.player_speed
        elif self.direction == "down":
            self.rect.y += TILESIZE //self.player_speed
        elif self.direction == "right":
            self.rect.x += TILESIZE//self.player_speed
        elif self.direction == "left":
            self.rect.x -= TILESIZE//self.player_speed

    def reset_player(self):
        self.moving = False
        self.rect.x = round(self.dest_x/32)*TILESIZE
        self.rect.y = round(self.dest_y/32)*TILESIZE

        self.dest_x, self.dest_y = 0, 0

    # Move cyclus.
    def update(self):
        if not self.moving:
            self.rect.x += self.vx * self.game.delta
            self.rect.y += self.vy * self.game.delta
        else:
            self.move()

    def path_walkable(self):
        for object in self.game.sprites["objects"]:
            if object.x*TILESIZE == self.dest_x and object.y*TILESIZE == self.dest_y:
                return False
        return True