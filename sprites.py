import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
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
        self.image.fill(BLACK)

        #Define rect and position
        self.rect = self.image.get_rect()
    
    def update(self):
        self.move()

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

        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)

            if hits:
                if self.xChange < 0:
                    self.rect.left = hits[0].rect.right
                if self.xChange > 0:
                    self.rect.right = hits[0].rect.left

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)

            if hits:
                if self.yChange < 0:
                    self.rect.top = hits[0].rect.bottom
                if self.yChange > 0:
                    self.rect.bottom = hits[0].rect.top

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
        self.image.fill(RED)

        #Define rect and position
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE