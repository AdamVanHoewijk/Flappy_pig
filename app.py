import pygame
import random

pygame.init()
pygame.font.init()
# Declared constants
DISPLAY_HEIGHT = 800
DISPLAY_WIDTH = 600
GRAVITY = 0.8
JUMP_VELOCITY = -15
PIPE_VELOCITY = 2
PIPE_FREQUENCY = 1200
PIPE_GAP = 0.28 * DISPLAY_HEIGHT

# Creates display
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Flappy bird')
clock = pygame.time.Clock()

#Loads images
pig_images = [pygame.image.load('pig1.png'), pygame.image.load('pig2.png'), pygame.image.load('pig3.png')]
for x in range(3):
    size = pig_images[x].get_rect().size
    pig_images[x] = pygame.transform.scale(pig_images[x], (int(0.1*size[0]), int(0.1*size[1])))

pipe_image = pygame.image.load('pipe.png')
pipe_image = pygame.transform.scale(pipe_image, tuple([int(0.6 * x) for x in pipe_image.get_rect().size]))

background_img = pygame.image.load('background.png')

# Starting position of pig
y = int(DISPLAY_HEIGHT * 0.5)
x = int(DISPLAY_WIDTH * 0.1)

# Current velocity of pig
velocity = 0
score = 0

# Keeps track of previous scores
high_score = 0

# Variables to control game flow
paused = False
running = True

# Variable to keep track and time when a new pipe should be made
pipe_displayed = False

# Font for text
font = pygame.font.Font('freesansbold.ttf', 32)

# Draws the pig at the given x y position and rotates image based on velocity
class Pig(pygame.sprite.Sprite):
    # Describes the order in which the different pig images should appear
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.count_loop = (0, 1, 2, 1)
        self.image = pig_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (int(DISPLAY_WIDTH*0.1), int(DISPLAY_HEIGHT/2))

    def update(self):
        global velocity
        global paused
        self.image = pig_images[self.count_loop[int(pygame.time.get_ticks() / 100) % 4]]
        if (velocity > 8):
            self.image = pig_images[1]
        self.image = pygame.transform.rotate(self.image, -velocity)
        #self.rect = self.image.get_rect()

        velocity += GRAVITY
        self.rect.y += int(velocity)

        if (self.rect.top <= 0):
            velocity = 1
        if (self.rect.bottom >= DISPLAY_HEIGHT):
            velocity = -3

        if len(pygame.sprite.spritecollide(self, sprites, False)) > 1:
            paused = True


# The sprite of a pipe
class Pipe(pygame.sprite.Sprite):

    def __init__(self, y, inverted, follow_pipe = None):
        pygame.sprite.Sprite.__init__(self)
        self.follow_pipe = follow_pipe
        if inverted:
            self.image = pygame.transform.rotate(pipe_image, 180)
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (DISPLAY_WIDTH,int(y))
            self.scored = False

        else:
            self.image = pipe_image
            self.rect = self.image.get_rect()
            self.rect.topleft = (DISPLAY_WIDTH, y)



    def update(self):
        global pig
        global score
        self.rect.x -= PIPE_VELOCITY
        if self.follow_pipe != None:
            self.rect.x = self.follow_pipe.rect.x
            if self.rect.x <= pig.rect.x and not self.scored:
                self.scored = True
                score += 1

def restart():
    global high_score
    global pig
    global score
    global paused
    sprites.empty()
    pig = Pig()
    sprites.add(pig)
    if score > high_score:
        high_score = score
    score = 0
    paused = False

sprites = pygame.sprite.Group()
pig = Pig()
sprites.add(pig)
# Main loop
while running:
    # Checks for button presses and acts upon that action
    for event in pygame.event.get():

        # Ends game if exit is pressed
        if event.type == pygame.QUIT:
            running = False

        # If space is pressed, give pig jump velocity
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = JUMP_VELOCITY
            elif event.key == pygame.K_r:
                restart()

    # Creates new pipes based on ticks
    a = int(pygame.time.get_ticks() / PIPE_FREQUENCY) % 2
    if a == 1 and not pipe_displayed:
        pipe_displayed = True
        pipe_y_pos = int(random.random() * DISPLAY_HEIGHT * 0.5 + 250)
        pipe = Pipe(pipe_y_pos, False)
        sprites.add(pipe)
        sprites.add(Pipe(pipe_y_pos - PIPE_GAP, True, pipe))
    elif a == 0:
        pipe_displayed = False

    for sprite in sprites:
        if sprite.rect.right <= 0:
            sprites.remove(sprite)


    # Updates sprites
    if not paused:
        sprites.update()

    # Draws display
    gameDisplay.fill((0,255,255))
    gameDisplay.blit(background_img,(0,0))

    sprites.draw(gameDisplay)

    textsurface = font.render(str(score), False, (255,255,255))
    gameDisplay.blit(textsurface,(DISPLAY_WIDTH//2 - textsurface.get_width(), int(DISPLAY_HEIGHT*0.05)))

    textsurface = font.render("High score: "+str(high_score), False, (255, 0, 0))
    gameDisplay.blit(textsurface, (int(DISPLAY_WIDTH*0.05), int(DISPLAY_HEIGHT * 0.05)))


    pygame.display.update()
    clock.tick(60)

pygame.quit()
