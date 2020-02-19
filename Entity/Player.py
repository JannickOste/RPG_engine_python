from Entity.Entity import Entity, TILESIZE


class Player(Entity):
    def __init__(self, game, x, y, npc_id):
        self.game = game
        super().__init__(game, x, y, npc_id, group=self.game.sprites["player"])

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
                if self.game.map_handler.is_map_changer(dest_x, dest_y):
                    self.game.map_handler.load(self.game.map_handler.new_map_name(dest_x, dest_y))

                # Reset movement check.
                self.moving = False
                self.running = False
                self.walkcount = 6
                # Put player at correct TILESIZE*TILESIZE(32*32) position.
                self.rect.x = round(self.dest_x / TILESIZE) * TILESIZE
                self.rect.y = round(self.dest_y / TILESIZE) * TILESIZE
