import pygame
import random
import time
import math
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
        self.image = self.game.character_spritesheet.get_sprite(3, 2, TILESIZE, TILESIZE)

        #Set direction and animation loop
        self.facing = "up"
        self.animationLoop = 1

        #Define lastAttackTime
        self.lastAttackTime = 0

        #Define rect and position
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.input()
        self.collide_enemies()
        self.animate()

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
                Attack(self.game, self.x, self.y - TILESIZE, "up")
                self.lastAttackTime = time.time()
            if self.facing == "down" and time.time() - self.lastAttackTime >= ATTACK_COOLDOWN:
                Attack(self.game, self.x, self.y + TILESIZE, "down")
                self.lastAttackTime = time.time()
            if self.facing == "right" and time.time() - self.lastAttackTime >= ATTACK_COOLDOWN:
                Attack(self.game, self.x + TILESIZE, self.y, "left")
                self.lastAttackTime = time.time()
            if self.facing == "left" and time.time() - self.lastAttackTime >= ATTACK_COOLDOWN:
                Attack(self.game, self.x - TILESIZE, self.y, "right")
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

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(3, 2, TILESIZE,TILESIZE),
                           self.game.character_spritesheet.get_sprite(35, 2, TILESIZE,TILESIZE),
                           self.game.character_spritesheet.get_sprite(68, 2, TILESIZE,TILESIZE)]

        up_animations = [self.game.character_spritesheet.get_sprite(3, 34, TILESIZE,TILESIZE),
                         self.game.character_spritesheet.get_sprite(35, 34, TILESIZE,TILESIZE),
                         self.game.character_spritesheet.get_sprite(68, 34, TILESIZE,TILESIZE)]

        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, TILESIZE,TILESIZE),
                           self.game.character_spritesheet.get_sprite(35, 98, TILESIZE,TILESIZE),
                           self.game.character_spritesheet.get_sprite(68, 98, TILESIZE,TILESIZE)]

        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, TILESIZE,TILESIZE),
                            self.game.character_spritesheet.get_sprite(35, 66, TILESIZE,TILESIZE),
                            self.game.character_spritesheet.get_sprite(68, 66, TILESIZE,TILESIZE)]

        #Check direction
        if self.facing == "down":
            #If standing still, set image
            if self.yChange == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, TILESIZE, TILESIZE)
            #If moving, change image according to animation loop
            else:
                self.image = down_animations[math.floor(self.animationLoop)]
                self.animationLoop += 0.1
                if self.animationLoop >= 3:
                    self.animationLoop = 1
        if self.facing == "up":
            if self.yChange == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, TILESIZE, TILESIZE)
            else:
                self.image = up_animations[math.floor(self.animationLoop)]
                self.animationLoop += 0.1
                if self.animationLoop >= 3:
                    self.animationLoop = 1
        if self.facing == "left":
            if self.xChange == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, TILESIZE, TILESIZE)
            else:
                self.image = left_animations[math.floor(self.animationLoop)]
                self.animationLoop += 0.1
                if self.animationLoop >= 3:
                    self.animationLoop = 1
        if self.facing == "right":
            if self.xChange == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, TILESIZE, TILESIZE)
            else:
                self.image = right_animations[math.floor(self.animationLoop)]
                self.animationLoop += 0.1
                if self.animationLoop >= 3:
                    self.animationLoop = 1

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
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

        #Create image and set animation loop
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
        self.animationLoop = 1
        self.direction = direction

        #Create rect
        self.rect = self.image.get_rect()
        self.rect.x = self.x + self.game.xOffset
        self.rect.y = self.y + self.game.yOffset

        #Set initial time
        self.initialTime = time.time()

    def update(self):
        self.collide_enemy()
        self.animate()

        #Move for camera
        self.rect.x = self.x + self.game.xOffset
        self.rect.y = self.y + self.game.yOffset
 
    def collide_enemy(self):
        #Check if collided with enemy and delete enemy
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

        if self.direction == "up":
            self.image = up_animations[math.floor(self.animationLoop)]
            self.animationLoop += 0.5
            if self.animationLoop >= 5:
                self.kill()
        if self.direction == "down":
            self.image = down_animations[math.floor(self.animationLoop)]
            self.animationLoop += 0.5
            if self.animationLoop >= 5:
                self.kill()
        if self.direction == "left":
            self.image = right_animations[math.floor(self.animationLoop)]
            self.animationLoop += 0.5
            if self.animationLoop >= 5:
                self.kill()
        if self.direction == "right":
            self.image = left_animations[math.floor(self.animationLoop)]
            self.animationLoop += 0.5
            if self.animationLoop >= 5:
                self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game

        #Define render layer
        self._layer = ENEMY_LAYER

        #Define groups
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        #Define image
        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK)

        #Define animation loop
        self.animationLoop = 1

        #Define movement variables
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.movement_loop = 0
        self.max_travel = random.randint(7, 50)
        self.facing = random.choice(["left", "right"])

        #Define rect and position
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()

        #Check direction
        if self.facing == "left":
            #Move and check if direction change is necesarry
            self.x -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "right"
        if self.facing == "right":
            #Move and check if direction change is necesarry
            self.x += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "left"

        #Apply move
        self.rect.x = self.x + self.game.xOffset
        self.rect.y = self.y + self.game.yOffset

    def animate(self):
        down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, TILESIZE,TILESIZE),
                           self.game.enemy_spritesheet.get_sprite(35, 2, TILESIZE,TILESIZE),
                           self.game.enemy_spritesheet.get_sprite(68, 2, TILESIZE,TILESIZE)]

        up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, TILESIZE,TILESIZE),
                         self.game.enemy_spritesheet.get_sprite(35, 34, TILESIZE,TILESIZE),
                         self.game.enemy_spritesheet.get_sprite(68, 34, TILESIZE,TILESIZE)]

        left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, TILESIZE,TILESIZE),
                           self.game.enemy_spritesheet.get_sprite(35, 98, TILESIZE,TILESIZE),
                           self.game.enemy_spritesheet.get_sprite(68, 98, TILESIZE,TILESIZE)]

        right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, TILESIZE,TILESIZE),
                            self.game.enemy_spritesheet.get_sprite(35, 66, TILESIZE,TILESIZE),
                            self.game.enemy_spritesheet.get_sprite(68, 66, TILESIZE,TILESIZE)]

        #Check direction
        if self.facing == "down":
            self.image = down_animations[math.floor(self.animationLoop)]
            self.animationLoop += 0.1
            if self.animationLoop >= 3:
                self.animationLoop = 1
        if self.facing == "up":
            self.image = up_animations[math.floor(self.animationLoop)]
            self.animationLoop += 0.1
            if self.animationLoop >= 3:
                self.animationLoop = 1
        if self.facing == "left":
            self.image = left_animations[math.floor(self.animationLoop)]
            self.animationLoop += 0.1
            if self.animationLoop >= 3:
                self.animationLoop = 1
        if self.facing == "right":
            self.image = right_animations[math.floor(self.animationLoop)]
            self.animationLoop += 0.1
            if self.animationLoop >= 3:
                self.animationLoop = 1

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.game = game

        #Define render layer
        self._layer = BLOCK_LAYER

        #define groups
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        #Define image
        self.image = self.game.terrain_spritesheet.get_sprite(768, 576, TILESIZE, TILESIZE)

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

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game

        #Set render layer
        self._layer = GROUND_LAYER

        #Set groups
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        #Set move variables
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        #Set image
        self.image = self.game.terrain_spritesheet.get_sprite(448, 352, TILESIZE, TILESIZE)

        #Set rect
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        #Move for camera
        self.rect.x = self.x + self.game.xOffset
        self.rect.y = self.y + self.game.yOffset

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, font):
        #Set font/fontsize
        self.font = font

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

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

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

