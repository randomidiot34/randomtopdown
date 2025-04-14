from config import *
from sprites import *
import pygame

class main_menu:
    def __init__(self, game):
        self.game = game

        #Create groups
        self.all_sprites = pygame.sprite.LayeredUpdates()

        #Create text
        self.textList = []
        self.title = Text(self.game, self , WIN_WIDTH/2, 75, BLACK, "RandomTopDown", self.game.font_arial128, True)
        self.textList.append(self.title)

        #Create buttons
        self.buttonList = []
        self.level1 = Button(self.game, self, 100, 175, 120, 100, WHITE, BLACK, "Level 1", self.game.font_arial32)
        self.buttonList.append(self.level1)
        self.level2 = Button(self.game, self, 250, 175, 120, 100, WHITE, BLACK, "Level 2", self.game.font_arial32)
        self.buttonList.append(self.level2)

    def update(self):

        #Check if button got pressed, change scene
        if self.level1.get_pressed():
            for sprite in self.all_sprites:
                sprite.kill()
            self.game.scene = level_1(self.game)
        if self.level2.get_pressed():
            for sprite in self.all_sprites:
                sprite.kill()
            self.game.scene = level_2(self.game)

    def draw(self):
        #Draw background
        self.game.screen.blit(self.game.background, (0, 0))

        self.all_sprites.draw(self.game.screen)

class level_1:
    def __init__(self, game):
        self.game = game

        #Set camera offset
        self.xOffset = 0
        self.yOffset = 0

        #Create camera
        self.camera = Camera(self)

        #Create groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()

        self.createTilemap(LEVEL1)

    def createTilemap(self, level):
        for i, row in enumerate(level):
            for j, column in enumerate(row):
                Ground(self.game, self, j, i)
                if column == "B":
                    Block(self.game, self, j, i, 1, 1)
                if column == "P":
                    self.player = Player(self.game, self, j, i)
                if column == "E":
                    Enemy(self.game, self, j, i)

    def die(self):
        for sprite in self.all_sprites:
                sprite.kill()
                pygame.mixer.stop()
        self.game.scene = main_menu(self.game)

    def update(self):
        self.all_sprites.update()
        self.camera.update()

    def draw(self):
        self.all_sprites.draw(self.game.screen)

class level_2:
    def __init__(self, game):
        self.game = game

        #Set camera offset
        self.xOffset = 0
        self.yOffset = 0

        #Create camera
        self.camera = Camera(self)

        #Create groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()

        self.createTilemap(LEVEL2)

    def createTilemap(self, level):
        for i, row in enumerate(level):
            for j, column in enumerate(row):
                Ground(self.game, self, j, i)
                if column == "B":
                    Block(self.game, self, j, i, 1, 1)
                if column == "P":
                    self.player = Player(self.game, self, j, i)
                if column == "E":
                    Enemy(self.game, self, j, i)

    def die(self):
        for sprite in self.all_sprites:
                sprite.kill()
                pygame.mixer.stop()
        self.game.scene = main_menu(self.game)

    def update(self):
        self.all_sprites.update()
        self.camera.update()

    def draw(self):
        self.all_sprites.draw(self.game.screen)