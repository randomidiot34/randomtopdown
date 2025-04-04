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

        #Import images
        self.background = pygame.image.load("img/background.png").convert()

        #Set fonts
        self.font_arial32 = pygame.font.Font("ARIAL.ttf", 32)
        self.font_arial128 = pygame.font.Font("ARIAL.ttf", 128)

        self.running = True
        self.playing = False

    def createTilemap(self, level):
        for i, row in enumerate(level):
            for j, column in enumerate(row):
                if column == "B":
                    Block(self, j, i, 1, 1)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "E":
                    Enemy(self, j, i)

    def intro_screen(self):
        intro = True
        
        title = self.font_arial128.render("Random Topdown", True, BLACK)
        title_rect = title.get_rect(center=([WIN_WIDTH/2, 75]))

        buttonList = []

        level1 = Button(100, 175, 120, 100, WHITE, BLACK, "Level 1", self.font_arial32)
        level2 = Button(250, 175, 120, 100, WHITE, BLACK, "Level 2", self.font_arial32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

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

            self.screen.blit(self.background)
            self.screen.blit(title, title_rect)
            self.screen.blit(level1.image, level1.rect)
            self.screen.blit(level2.image, level2.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def events(self):
        #Handle events
        for event in pygame.event.get():
            #Quit
            if event.type == pygame.QUIT:
                pygame.quit()

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
        #When player died, delete all sprites and go back to menu screen
        for sprite in self.all_sprites:
            sprite.kill()
        self.intro_screen()

game = Game()

game.intro_screen()

pygame.quit()
