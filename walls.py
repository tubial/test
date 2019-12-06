#! python3
# pygame_boilerplate.py
# Provides template code on which to build

import pygame

pygame.init()

# CONSTANTS --------
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_TITLE = "Walls"
REFRESH_RATE = 60

BGCOLOUR = (0, 0, 0)
WHITE =    (0xFF, 0xFF, 0xFF)
BLACK =    ( 0x0,  0x0,  0x0)
RED =      (0xFF,  0x0,  0x0)
GREEN =    ( 0x0, 0xFF,  0x0)
BLUE =     ( 0x0,  0x0, 0xFF)

# Class     --------
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.transform.scale(
            pygame.image.load("link.png").convert(),
            (64, 64)
        )
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.walls = None
        self.vel_x = 0
        self.vel_y = 0

    def update(self):
        # Update the location of our player
        # Left and Right Movement
        self.rect.x += self.vel_x

        wall_hit_list = pygame.sprite.spritecollide(
            self, self.walls, False
        )
        for wall in wall_hit_list:
            # If we're moving to the right
            # line up the right side of the sprite
            # to the left side of the wall
            if self.vel_x > 0:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right


        self.rect.y += self.vel_y

        wall_hit_list = pygame.sprite.spritecollide(
            self, self.walls, False
        )
        for wall in wall_hit_list:
            if self.vel_y > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom

    def change_vel(self, x, y):
        self.vel_x += x
        self.vel_y += y

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Functions --------

def main():
    # STATIC Variables -------
    PLAYER_SPEED = 3
    
    # LOCAL Variables  -------
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    done = False # controls our main loop

    pygame.display.set_caption(WINDOW_TITLE)

    wall_sprite_list = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()

    wall = Wall(0, 0, 10, 600)
    wall_sprite_list.add(wall)
    all_sprites_list.add(wall)

    wall = Wall(10, 0, 790, 10)
    wall_sprite_list.add(wall)
    all_sprites_list.add(wall)

    wall = Wall(10, 400, 300, 10)
    wall_sprite_list.add(wall)
    all_sprites_list.add(wall)

    # Add the player
    player = Player(50, 50)
    player.walls = wall_sprite_list
    all_sprites_list.add(player)

    # Main loop
    while not done:
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.change_vel(0, -PLAYER_SPEED)
                elif event.key == pygame.K_DOWN:
                    player.change_vel(0, PLAYER_SPEED)
                elif event.key == pygame.K_LEFT:
                    player.change_vel(-PLAYER_SPEED, 0)
                elif event.key == pygame.K_RIGHT:
                    player.change_vel(PLAYER_SPEED, 0)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.change_vel(0, PLAYER_SPEED)
                elif event.key == pygame.K_DOWN:
                    player.change_vel(0, -PLAYER_SPEED)
                elif event.key == pygame.K_LEFT:
                    player.change_vel(PLAYER_SPEED, 0)
                elif event.key == pygame.K_RIGHT:
                    player.change_vel(-PLAYER_SPEED, 0)

        # Game Logic --------
        all_sprites_list.update()

        # Drawing --------
        screen.fill(BGCOLOUR)
        
        all_sprites_list.draw(screen)

        pygame.display.flip() # update the screen

        # Clock Tick -------
        clock.tick(REFRESH_RATE)

if __name__ == "__main__":
    main()