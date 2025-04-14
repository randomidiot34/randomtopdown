import pygame
import sys
from sprites import *
from config import *
from scenes import *

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

        #Set initial scene
        self.scene = main_menu(self)

        #Start game
        self.running = True

    def events(self):
        #Handle events
        for event in pygame.event.get():
            #Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw(self):
        #Draw all sprites
        self.screen.fill(WHITE)
        self.scene.draw()
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        self.running

        #Gameloop
        while self.running:
            self.events()
            self.scene.update()
            self.draw()

game = Game()

game.main()

pygame.quit()
