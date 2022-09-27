import pygame

pygame.init()

from pygame.rect import *
from pygame.locals import *

moving = False

rect = Rect(50, 60, 200, 80)
screen = pygame.display.set_mode((600, 800))

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                moving = True
        elif event.type == MOUSEBUTTONUP:
            moving = False
        elif event.type == MOUSEMOTION and moving:
            rect.move_ip(event.rel)
    screen.fill((127, 127, 127))
    pygame.draw.rect(screen, (255, 0, 0), rect)

    if moving:
        pygame.draw.rect(screen, (0, 0, 255), rect, 4)

    pygame.display.flip()

pygame.quit()
