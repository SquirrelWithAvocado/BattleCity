from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT
import pygame

pygame.init()

from pygame.rect import *
from pygame.locals import *
rect0 = Rect(50, 60, 200, 80)
rect = rect0.copy()

dir = {
    K_LEFT: (-5, 0), 
    K_RIGHT: (5, 0), 
    K_UP: (0, -5), 
    K_DOWN: (0, 5)
}

screen = pygame.display.set_mode((600, 800))

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key in dir:
                v = dir[event.key]
                rect.move_ip(v)
    screen.fill((127, 127, 127))

    pygame.draw.rect(screen, (0, 0, 255), rect0, 1)
    pygame.draw.rect(screen, (255, 0, 0), rect, 4)
    pygame.display.flip()
    
pygame.quit()
