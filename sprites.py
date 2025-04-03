import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game

        #Define render layer
        self._layer = PLAYER_LAYER

        #define groups
        self.groups = self.game.all_sprites, self.game.player
        pygame.sprite.Sprite.__init__(self, self.groups)

        #Define move variables
        self.yChange = 0
        self.xChange = 0

        #Define image
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill(GREEN)

        #Define rect and position
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        self.move()
        self.collide_enemies()

        #Apply move and check for collisions
        self.rect.y += self.yChange
        self.collide_blocks("y")
        self.rect.x += self.xChange
        self.collide_blocks("x")

        #Reset move
        self.yChange = 0
        self.xChange = 0

    def move(self):
        #Get pressed keys
        keys = pygame.key.get_pressed()

        #Check key
        if keys[pygame.K_w]:
            self.yChange -= PLAYER_SPEED
        if keys[pygame.K_s]:
            self.yChange += PLAYER_SPEED
        if keys[pygame.K_a]:
            self.xChange -= PLAYER_SPEED
        if keys[pygame.K_d]:
            self.xChange += PLAYER_SPEED

    def collide_blocks(self, direction):
        #Check for collisions
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)

        #Check direction
        if direction == "x":
            #Check if player collided and set position
            if hits:
                if self.xChange < 0:
                    self.rect.left = hits[0].rect.right
                if self.xChange > 0:
                    self.rect.right = hits[0].rect.left
        if direction == "y":
            #Check if player collided and set position
            if hits:
                if self.yChange < 0:
                    self.rect.top = hits[0].rect.bottom
                if self.yChange > 0:
                    self.rect.bottom = hits[0].rect.top

    def collide_enemies(self):
        #Check for collision
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)

        #If player collided, end game
        if hits:
            self.game.running = False

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.game = game

        #Define render layer
        self._layer = BLOCK_LAYER

        #define groups
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        #Define image
        self.image = pygame.Surface([width * TILESIZE, height * TILESIZE])
        self.image.fill(BLACK)

        #Define rect and position
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game

        #Define render layer
        self._layer = ENEMY_LAYER

        #Define groups
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        #Define image
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill(RED)

        #Define rect and position
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
            pass
