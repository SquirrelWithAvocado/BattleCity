from turtle import Screen
import pygame
from pygame.locals import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)

ball = pygame.image.load(r'examples\images\football1.jpg')

size = 640, 320
width, height = size

pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

rect = ball.get_rect()
speed = [2, 2]

run = True

while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
    
    rect = rect.move(speed)
    if rect.left < 0 or rect.right > width:
        speed[0] = - speed[0]
    if rect.top < 0 or rect.bottom > height:
        speed[1] = - speed[1]
    
    screen.fill(GREEN)
    pygame.draw.rect(screen, RED, rect, 1)
    screen.blit(ball, rect)
    pygame.display.update()

    clock.tick(30)

pygame.quit()