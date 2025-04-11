import pygame
import sys
from sprites import *
from config import *

class Game:
    def __init__(self):
        pygame.init()

        #Set screen stuff
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption(WIN_CAPTION)
        self.clock = pygame.time.Clock()

        #Import images
        self.background = pygame.image.load("img/background.png").convert()

        #Import spritesheets
        self.character_spritesheet = Spritesheet("img/character.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.enemy_spritesheet = Spritesheet("img/enemy.png")
        self.attack_spritesheet = Spritesheet("img/attack.png")

        #Set fonts
        self.font_arial32 = pygame.font.Font("font/ARIAL.ttf", 32)
        self.font_arial128 = pygame.font.Font("font/ARIAL.ttf", 128)

        #Import sounds
        self.sfx_walk = pygame.mixer.Sound("sfx/walk.mp3")
        self.sfx_attack_normal = pygame.mixer.Sound("sfx/attack_normal.mp3")
        self.sfx_enemy_kill = pygame.mixer.Sound("sfx/enemy_kill.mp3")

        self.running = True
        self.playing = False

    def createTilemap(self, level):
        for i, row in enumerate(level):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i, 1, 1)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "E":
                    Enemy(self, j, i)

    def intro_screen(self):
        intro = True

        textList = []

        title = Text(game, WIN_WIDTH/2, 75, BLACK, "RandomTopDown", self.font_arial128, True)
        textList.append(title)

        buttonList = []

        level1 = Button(game, 100, 175, 120, 100, WHITE, BLACK, "Level 1", self.font_arial32)
        buttonList.append(level1)
        level2 = Button(game, 250, 175, 120, 100, WHITE, BLACK, "Level 2", self.font_arial32)
        buttonList.append(level2)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if level1.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                self.playing = True
                self.main(LEVEL1)
            if level2.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                self.playing = True
                self.main(LEVEL2)

            self.screen.blit(self.background, (0,0))
            for text in textList:
                text.draw()
            for button in buttonList:
                button.draw()
            self.clock.tick(FPS)
            pygame.display.update()

    def events(self):
        #Handle events
        for event in pygame.event.get():
            #Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        #Update all sprites
        self.camera.update()
        self.all_sprites.update()

    def draw(self):
        #Draw all sprites
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self, level):
        #Set groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()

        #Set camera offset
        self.xOffset = 0
        self.yOffset = 0

        #Load tilemap and create camera
        self.createTilemap(level)
        self.camera = Camera(self)

        #Gameloop
        while self.playing:
            self.events()
            self.update()
            self.draw()

        #When player dies, delete all sprites and go back to menu screen
        for sprite in self.all_sprites:
            pygame.mixer.stop()
            sprite.kill()
        self.intro_screen()

game = Game()

game.intro_screen()

pygame.quit()
