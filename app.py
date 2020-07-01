import pygame
pygame.init()

DISPLAY_HEIGHT = 800
DISPLAY_WIDTH = 600
GRAVITY = 0.7
JUMP_VELOCITY = -15

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
pygame.display.set_caption('Flappy bird')
clock = pygame.time.Clock()
images = (pygame.image.load('pig1.png'),pygame.image.load('pig2.png'),pygame.image.load('pig3.png'))
black = (0,0,0)

count_loop = (0,1,2,1)

def bird(x, y):
    image = images[count_loop[int(pygame.time.get_ticks()/100)%4]]
    img_size = image.get_rect().size
    image = pygame.transform.scale(image, tuple([int(0.1*x) for x in img_size]))
    gameDisplay.blit(image,(x,y))

y = int(DISPLAY_HEIGHT * 0.5)
x = int(DISPLAY_WIDTH * 0.2)
velocity = 0
animation_count = 0

running = True
while running:

    if (y >= DISPLAY_HEIGHT):
        velocity = 0
        y = DISPLAY_HEIGHT
    else:
        velocity += GRAVITY


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = JUMP_VELOCITY

    y += velocity
    gameDisplay.fill(black)
    bird(x, int(y))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
