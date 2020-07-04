import pygame
import random
import Sprites

class Game:

    def __init__(self):
        self.high_score = 0
        self.DISPLAY_HEIGHT = 800
        self.DISPLAY_WIDTH = 600
        self.GRAVITY = 0.8
        self.JUMP_VELOCITY = -15
        self.PIPE_VELOCITY = 2
        self.PIPE_FREQUENCY = 250
        self.PIPE_GAP = 0.28 * self.DISPLAY_HEIGHT
        self.pig_sprites = pygame.sprite.Group()
        self.pipe_sprites = pygame.sprite.Group()
        self.pig_sprites.add(Sprites.Pig(self))

        self.background_img = pygame.image.load('background.png')
        self.high_score = 0
        self.paused = False
        self.running = True
        pygame.init()
        pygame.font.init()
        self.gameDisplay = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        pygame.display.set_caption('Flappy bird')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 32)

    def restart(self):
        self.pipe_sprites.empty()
        self.pig_sprites.empty()
        self.pig_sprites.add(Sprites.Pig(self))
        self.paused = False
        self.add_pipe()

    def add_pipe(self):
        pipe_y_pos = int(random.random() * self.DISPLAY_HEIGHT * 0.5 + 250)
        pipe = Sprites.Pipe(pipe_y_pos, self)
        self.pipe_sprites.add(pipe)
        self.pipe_sprites.add(Sprites.Pipe(pipe_y_pos - self.PIPE_GAP, self, pipe))

    def main(self):

        self.add_pipe()
        # Main loop
        while self.running:

            alive_list = []
            for pig in self.pig_sprites:
                alive_list.append(pig.alive)
            if not any(alive_list):
                self.paused = True
            # Creates new pipes
            if self.pipe_sprites.sprites()[-1].rect.left <= self.DISPLAY_WIDTH - self.PIPE_FREQUENCY:
                self.add_pipe()

            for sprite in self.pipe_sprites:
                if sprite.rect.right <= 0:
                    self.pipe_sprites.remove(sprite)

            # Checks for button presses and acts upon that action
            for event in pygame.event.get():

                # Ends game if exit is pressed
                if event.type == pygame.QUIT:
                    self.running = False

                # If space is pressed, give pig jump velocity
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for pig in self.pig_sprites:
                            pig.jump()
                    elif event.key == pygame.K_r:
                        self.restart()

            # Updates sprites
            if not self.paused:
                self.pipe_sprites.update()
                self.pig_sprites.update()

            # Draws display
            self.gameDisplay.fill((0,255,255))
            self.gameDisplay.blit(self.background_img,(0,0))

            self.pipe_sprites.draw(self.gameDisplay)
            self.pig_sprites.draw(self.gameDisplay)

            textsurface = self.font.render("High score: "+str(self.high_score), False, (255, 0, 0))
            self.gameDisplay.blit(textsurface, (int(self.DISPLAY_WIDTH*0.05), int(self.DISPLAY_HEIGHT * 0.05)))

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
game = Game()
game.main()