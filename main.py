import pygame

from actors import Player, Enemy

# Init the pygame
pygame.init()

# Create the screen
WIDTH = 600
HEIGHT = 480
FPS = 60

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Title and icon of the windows
pygame.display.set_caption("Space Invaders")

# Instantiate sprites
player = Player(path='media/link', tiles_per_move=8, frames=5, speed=5, inf_scroll=False, surface=screen, pos=(100, 100))
enemy = Enemy(screen, inf_scroll=True)

enemies = pygame.sprite.Group(enemy)
all_sprites = pygame.sprite.Group(player, enemies)

# Game loop
running = True
iddle_move = 'IDDLE_DOWN'
while running:
    # Set the FPS
    clock.tick(FPS)

    # RGB - Red, Green, Blue
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            event_type = pygame.KEYDOWN
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                iddle_move = 'IDDLE_UP'
            if event.key == pygame.K_s:
                iddle_move = 'IDDLE_DOWN'
            if event.key == pygame.K_a:
                iddle_move = 'IDDLE_LEFT'
            if event.key == pygame.K_d:
                iddle_move = 'IDDLE_RIGHT'
        # elif event.type == pygame.MOUSEMOTION:
        #     enemy.rect.center = event.pos

    enemy.update()
    enemy.draw()

    player.draw()
    player.update(iddle_move)

    if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask):
        pygame.display.set_caption('collision')
    else:
        pygame.display.set_caption('no collision')

    # Update the screen in every loop
    pygame.display.update()

pygame.quit()
