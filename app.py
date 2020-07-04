import os
import neat
import pygame
import random
import Sprites

class Game:

    def __init__(self):
        self.high_score = 0
        self.DISPLAY_HEIGHT = 800
        self.DISPLAY_WIDTH = 600
        self.GRAVITY = 1.2
        self.JUMP_VELOCITY = -16
        self.PIPE_VELOCITY = 2
        self.PIPE_FREQUENCY = 270
        self.PIPE_GAP = 0.24 * self.DISPLAY_HEIGHT
        self.pig_sprites = pygame.sprite.Group()
        self.pipe_sprites = pygame.sprite.Group()
        self.score = 0
        self.background_img = pygame.image.load('background.png')
        self.high_score = 0
        self.paused = False
        self.running = True
        pygame.init()
        pygame.font.init()
        self.gameDisplay = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        pygame.display.set_caption('Flappy pig')
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
generation = 0
def main(genomes, config):
    global generation
    generation += 1
    nets = []
    pigs = []
    ge = []
    game = Game()
    clock_tick = 60

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        pig = Sprites.Pig(game)
        pigs.append(pig)
        game.pig_sprites.add(pig)
        g.fitness = 0
        ge.append(g)



    game.add_pipe()
    # Main loop
    while game.running:
        alive_list = []
        for pig in game.pig_sprites:
            alive_list.append(pig.alive)
        if not any(alive_list):
            game.paused = True

        if len(pigs) == 0:
            break
            game.running = False

        # Creates new pipes
        if game.pipe_sprites.sprites()[-1].rect.left <= game.DISPLAY_WIDTH - game.PIPE_FREQUENCY:
            game.add_pipe()

        # Removes offscreen pipes
        for sprite in game.pipe_sprites:
            if sprite.rect.right <= 0:
                game.pipe_sprites.remove(sprite)

        # Checks for button presses and acts upon that action
        for event in pygame.event.get():
            # Ends game if exit is pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if clock_tick == 1000:
                    clock_tick = 60
                else:
                    clock_tick = 1000



        # Updates sprites
        if not game.paused:
            game.pipe_sprites.update()
            game.pig_sprites.update()

        for pipe in game.pipe_sprites:
            if not pipe.passed and pipe.follow_pipe != None:
                current_pipe = pipe
                for x, pig in enumerate(pigs):

                    ge[x].fitness += 0.1 + pig.adjust_fitness()

                    outputs = nets[x].activate((pipe.rect.bottom - pig.rect.top
                                                , pipe.follow_pipe.rect.top - pig.rect.bottom
                                                ))
                    if outputs[0] > 0:
                        pig.jump()
                break

        for x , pig in enumerate(pigs):
            if pig.collided():
                pigs.pop(x)
                nets.pop(x)
                ge.pop(x)
                game.pig_sprites.remove(pig)




        # Draws display
        game.gameDisplay.fill((255,255,255))
        game.gameDisplay.blit(game.background_img,(0,0))

        game.pipe_sprites.draw(game.gameDisplay)
        game.pig_sprites.draw(game.gameDisplay)

        textsurface = game.font.render("Score: "+str(game.score), False, (255, 255, 255))
        game.gameDisplay.blit(textsurface, (int(game.DISPLAY_WIDTH - textsurface.get_width()-20), int(game.DISPLAY_HEIGHT * 0.05)))

        textsurface = game.font.render("Generation: " + str(generation), False, (255, 255, 255))
        game.gameDisplay.blit(textsurface,
                              (int(game.DISPLAY_WIDTH - textsurface.get_width() - 20), int(game.DISPLAY_HEIGHT * 0.1)))

        if clock_tick == 60:
            textsurface = game.font.render("Press button to speed up", False, (255, 255, 255))
            game.gameDisplay.blit(textsurface,
                                  (int(game.DISPLAY_WIDTH//2 - textsurface.get_width()//2), int(game.DISPLAY_HEIGHT * 0.95)))

        pygame.display.update()
        game.clock.tick(clock_tick)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())
    winner = p.run(main,100)




local_dir = os.path.dirname(__file__)
run(os.path.join(local_dir, "config file.txt"))
