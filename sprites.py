import pygame
import random
import time
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
        self.y = y * TILESIZE
        self.x = x * TILESIZE

        #Define image
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.image.fill(GREEN)

        #Set direction
        self.facing = "up"

        #Define lastAttackTime
        self.lastAttackTime = 0

        #Define rect and position
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.input()
        self.collide_enemies()

        # Apply vertical movement and check for collisions
        self.rect.y += self.yChange
        self.collide_blocks("y")
        self.y += self.yChange

        # Apply horizontal movement and check for collisions
        self.rect.x += self.xChange
        self.collide_blocks("x")
        self.x += self.xChange

        # Update the rect position based on the camera offset
        self.rect.x = self.x + self.game.xOffset
        self.rect.y = self.y + self.game.yOffset

        #Reset move
        self.yChange = 0
        self.xChange = 0

    def input(self):
        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_w]:
            self.yChange -= PLAYER_SPEED
            self.facing = "up"
        if keys[pygame.K_s]:
            self.yChange += PLAYER_SPEED
            self.facing = "down"
        if keys[pygame.K_a]:
            self.xChange -= PLAYER_SPEED
            self.facing = "left"
        if keys[pygame.K_d]:
            self.xChange += PLAYER_SPEED
            self.facing = "right"

        # Attack
        if keys[pygame.K_SPACE]:
            if self.facing == "up" and time.time() - self.lastAttackTime >= ATTACK_COOLDOWN:
                Attack(self.game, self.x, self.y - TILESIZE)
                self.lastAttackTime = time.time()
            if self.facing == "down" and time.time() - self.lastAttackTime >= ATTACK_COOLDOWN:
                Attack(self.game, self.x, self.y + TILESIZE)
                self.lastAttackTime = time.time()
            if self.facing == "right" and time.time() - self.lastAttackTime >= ATTACK_COOLDOWN:
                Attack(self.game, self.x + TILESIZE, self.y)
                self.lastAttackTime = time.time()
            if self.facing == "left" and time.time() - self.lastAttackTime >= ATTACK_COOLDOWN:
                Attack(self.game, self.x - TILESIZE, self.y)
                self.lastAttackTime = time.time()

    def collide_blocks(self, direction):
        # Check for collisions
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)

        # Check direction
        if direction == "x":
            # Check if player collided and set position
            if hits:
                if self.xChange < 0:
                    self.rect.left = hits[0].rect.right
                if self.xChange > 0:
                    self.rect.right = hits[0].rect.left
                # Update the player's actual position
                self.x = self.rect.x - self.game.xOffset
                self.xChange = 0
        if direction == "y":
            # Check if player collided and set position
            if hits:
                if self.yChange < 0:
                    self.rect.top = hits[0].rect.bottom
                if self.yChange > 0:
                    self.rect.bottom = hits[0].rect.top
                # Update the player's actual position
                self.y = self.rect.y - self.game.yOffset
                self.yChange = 0

    def collide_enemies(self):
        #Check for collision
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)

        #If player collided, end game
        if hits:
            self.game.playing = False

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

        #Define move variabels for camera
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        #Define rect and position
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        #Move block for camera
        self.rect.x = self.x + self.game.xOffset
        self.rect.y = self.y + self.game.yOffset

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

        #Define movement variables
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.movement_loop = 0
        self.max_travel = random.randint(7, 50)
        self.facing = random.choice(["l", "r"])

        #Define rect and position
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        #Check direction
        if self.facing == "l":
            #Move and check if direction change is necesarry
            self.x -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "r"
        if self.facing == "r":
            #Move and check if direction change is necesarry
            self.x += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "l"

        #Apply move
        self.rect.x = self.x + self.game.xOffset
        self.rect.y = self.y + self.game.yOffset

class Camera:
    def __init__(self, game):
        self.game = game

    def update(self):
        #Check if player moved past border
        if self.game.player.rect.top < CAMERA_BORDER_TOP:
            self.game.yOffset += PLAYER_SPEED
        if self.game.player.rect.bottom > CAMERA_BORDER_BOTTOM:
            self.game.yOffset -= PLAYER_SPEED
        if self.game.player.rect.left < CAMERA_BORDER_LEFT:
            self.game.xOffset += PLAYER_SPEED
        if self.game.player.rect.right > CAMERA_BORDER_RIGHT:
            self.game.xOffset -= PLAYER_SPEED

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        #Set font/fontsize
        self.font = pygame.font.Font("ARIAL.ttf", fontsize)

        #Set other variables
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg
        self.content = content

        #Set image
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.bg)
        
        #Set rect
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        #Set text
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=[self.width/2, self.height/2])
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        #Set render layer
        self._layer = ATTACK_LAYER

        #Set groups
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        #Create image
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLUE)

        #Create rect
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        #Set initial time
        self.initialTime = time.time()

    def update(self):
        self.collide_enemy()

        #Kill attack if linger time has passed
        if time.time() - self.initialTime >= ATTACK_LINGER_TIME:
            self.kill()

        #Move for camera
        self.rect.x = self.x + self.game.xOffset
        self.rect.y = self.y + self.game.yOffset
 
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
