import pygame
#Loads images
pig_images = [pygame.image.load('pig1.png'), pygame.image.load('pig2.png'), pygame.image.load('pig3.png')]
for x in range(3):
    size = pig_images[x].get_rect().size
    pig_images[x] = pygame.transform.scale(pig_images[x], (int(0.1*size[0]), int(0.1*size[1])))

count_loop = (0, 1, 2, 1)

class Pig(pygame.sprite.Sprite):
    # Describes the order in which the different pig images should appear
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.extra_fitness = 0
        self.alive = True
        self.score = 0
        self.velocity = 0
        self.game = game
        self.image = pig_images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (int(game.DISPLAY_WIDTH*0.1), int(game.DISPLAY_HEIGHT/2))

    def jump(self):
        self.velocity = self.game.JUMP_VELOCITY

    def update(self):
        global count_loop
        self.image = pig_images[count_loop[int(pygame.time.get_ticks() / 100) % 4]]
        if (self.velocity > 8):
            self.image = pig_images[1]
        self.image = pygame.transform.rotate(self.image, - self.velocity * 1.4)
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity += self.game.GRAVITY
        self.rect.y += int(self.velocity)

        if not self.alive:
            self.rect.x -= self.game.PIPE_VELOCITY


    def collided(self):
        if pygame.sprite.spritecollide(self, self.game.pipe_sprites, False):
            if pygame.sprite.spritecollide(self, self.game.pipe_sprites, False, pygame.sprite.collide_mask):
                if self.score > self.game.high_score:
                    self.game.high_score = self.score
                return True

        elif self.rect.top <= 0 or self.rect.top >= self.game.DISPLAY_HEIGHT:
            return True
        return False

    def adjust_fitness(self):
        res = self.extra_fitness
        self.extra_fitness = 0
        return res

pipe_image = pygame.image.load('pipe.png')
pipe_image = pygame.transform.scale(pipe_image, tuple([int(0.6 * x) for x in pipe_image.get_rect().size]))

# The sprite of a pipe
class Pipe(pygame.sprite.Sprite):

    def __init__(self, y, game, follow_pipe = None):
        pygame.sprite.Sprite.__init__(self)
        self.follow_pipe = follow_pipe
        self.game = game
        self.passed = False
        if self.follow_pipe != None:
            self.image = pygame.transform.rotate(pipe_image, 180)
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (self.game.DISPLAY_WIDTH,int(y))
            self.scored = False

        else:
            self.image = pipe_image
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.game.DISPLAY_WIDTH, y)

    def update(self):
        self.rect.x -= self.game.PIPE_VELOCITY
        if self.follow_pipe != None:
            self.rect.x = self.follow_pipe.rect.x
            for pig in self.game.pig_sprites:
                if self.rect.x <= pig.rect.x and not self.scored:
                    self.scored = True
                    self.game.score += 1
                    pig.extra_fitness += 5
                    self.passed = False
