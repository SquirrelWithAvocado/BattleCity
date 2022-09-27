from typing import Sequence
import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((640, 320))

start = (0, 0)
size = (0, 0)
drawing = False
rect_list = []

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == MOUSEBUTTONDOWN:
            print(event)
            start = event.pos
            size = 0, 0
            drawing = True
        elif event.type == MOUSEBUTTONUP:
            end = event.pos
            size = end[0] - start[0], end[1] - start[1]
            rect = pygame.Rect(start, size)
            rect_list.append(rect)
            drawing = False
            print(event)
        elif event.type == MOUSEMOTION and drawing:
            end = event.pos
            size = end[0] - start[0], end[1] - start[1]

    screen.fill((127, 127, 127))
    
    for rect in rect_list:
        pygame.draw.rect(screen, (255, 0, 0), rect, 3)

    pygame.draw.ellipse(screen, (0, 255, 0), (100, 60, 160, 100), 5)
    pygame.draw.aaline(screen, (255, 0, 0), (250, 100), (250, 200))
    # pygame.draw.polygon(screen, (255, 0, 0), [(20, 20), (50, 25), (80, 320)], 1)

    pygame.display.update()
    