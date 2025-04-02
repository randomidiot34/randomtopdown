import pygame
from sprites import *
from config import *

class Game:
    def __init__(self):
        pygame.init()

        #Set screen stuff
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption(WIN_CAPTION)
        self.clock = pygame.time.Clock()

        #Set groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()

        #Create entities
        Player(self)
        Block(self, 2, 2, 2, 2)

        #Start game
        self.running = True

    def events(self):
        #Handle events
        for event in pygame.event.get():
            #Quit
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        #Update all sprites
        self.all_sprites.update()
        
    def draw(self):
        #Draw all sprites
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #Gameloop
        while self.running:
            self.events()
            self.update()
            self.draw()

game = Game()

game.main()

pygame.quit()
