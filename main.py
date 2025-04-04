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

        #Set fonts
        self.font_arial32 = pygame.font.Font("ARIAL.ttf", 32)

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
        
        title = self.font_arial32.render("Random Topdown", True, BLACK)
        title_rect = title.get_rect()

        play_button = Button(10, 50, 100, 50, WHITE, BLACK, "PLAY", 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                self.playing = True
                self.main(TILEMAP)

            self.screen.fill(WHITE)
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
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
