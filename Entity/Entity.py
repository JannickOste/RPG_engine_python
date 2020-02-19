from Gfx.SpriteTemplate import SpriteTemplate
from Misc.Settings import *
import pygame as pg
from Misc.Settings import *
from random import choice


class Entity(SpriteTemplate):
    def __init__(self, game, x, y, npc_id, group=None):
        self.game = game
        self.npc_id = npc_id
        self.walk_image = self.load_walk_images(npc_id)
        group = group if group is not None else self.game.sprites["npcs"]
        super().__init__(game, x, y, group, self.walk_image[0][1])

        self.direction = "down"
        self.moving, self.running = False, False

        self.vel = pg.math.Vector2(0, 0)
        self.vx, self.vy = 0, 0
        self.dest_x, self.dest_y = 0, 0
        self.prev_x, self.prev_y = 0, 0
        self.next_walk_time = random_next_time()
        self.walkcount = 0

        self.speed = TILESIZE // PLAYER_SPEED


    # Move cyclus.
    def update(self):
        if not self.moving:
            self.rect.x += self.vx * self.game.delta
            self.rect.y += self.vy * self.game.delta
        else:
            self.move(x=1)

    def load_walk_images(self, npc_id):
        tile_set = []
        for row in self.game.sprite_handler.load_spriteset(npc_id):
            cur_row = []
            for tile in row:
                cur_row.append(self.game.sprite_handler.get_tile(tile))

            tile_set.append(cur_row)

        return tile_set

    def get_walk_image(self, entity):
        # Load current image and required tile_id's for movement.
        image_set = entity.walk_image
        image = entity.image

        # If player movement -> update image.
        if entity.moving:
            direction = entity.direction
            walkcount = self.walkcount // 3

            image = image_set[0][walkcount] if direction == "down" else image_set[1][walkcount] if direction == "left" \
                else image_set[2][walkcount] if direction == "right" else image_set[3][walkcount]

            # @todo: Have to look into running image is glitched.
            if self.walkcount < 8:
                self.walkcount += 1
            else:
                self.walkcount = 0

        entity.image = image

        return image

    def move_animation(self):
        speed = self.speed//1.3 if not self.running else self.speed
        if self.moving:
            if self.direction == "up":
                self.rect.y += -speed
            elif self.direction == "down":
                self.rect.y += speed
            elif self.direction == "right":
                self.rect.x += speed
            elif self.direction == "left":
                self.rect.x -= speed

    def move(self, x=0, y=0):
        moving = self.moving
        cur_x, cur_y = self.get_pos()

        direction = "left" if 0 > x else "right" if x > 0 else "down" if y > 0 else "up"
        dest_x = (cur_x - 1) * TILESIZE if direction == "left" \
            else (cur_x + 1) * TILESIZE if direction == "right" else cur_x * TILESIZE
        dest_y = (cur_y - 1) * TILESIZE if direction == "up" \
            else (cur_y + 1) * TILESIZE if direction == "down" else cur_y * TILESIZE

        # If not moving set destination coordinates and initiate walk.
        if not moving and any([x > 0, x < 0]) or any([y > 0, y < 0]) and self.valid_step(dest_x, dest_y):
            # Movement positions
            self.direction = direction
            self.dest_x = dest_x
            self.dest_y = dest_y
            # Velocity
            self.vx, self.vy = 0, 0

            # If path not adjective move to path.
            if self.valid_step(dest_x, dest_y):
                self.moving = True
        elif self.moving:
            self.move_animation()

            reset = False
            # Check or entity has reached it's destination.
            if self.direction == "up":
                reset = True if self.rect.y <= self.dest_y else False
            elif self.direction == "down":
                reset = True if self.rect.y >= self.dest_y else False
            elif self.direction == "left":
                reset = True if self.rect.x <= self.dest_x else False
            elif self.direction == "right":
                reset = True if self.rect.x >= self.dest_x else False

            if reset:
                if self.game.map_handler.is_map_changer():
                    self.game.map_handler.load()

                # Reset movement check.
                self.moving = False
                self.running = False
                self.walkcount = 6
                # Put player at correct TILESIZE*TILESIZE(32*32) position.
                self.rect.x = round(self.dest_x / TILESIZE) * TILESIZE
                self.rect.y = round(self.dest_y / TILESIZE) * TILESIZE

    def valid_step(self, dest_x, dest_y):
        for game_object in self.game.sprites["objects"]:

            if all([dest_x // TILESIZE == game_object.x, dest_y // TILESIZE == game_object.y]):
                return game_object.walkable

        return True