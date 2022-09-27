import pygame, sys
sys.path.append(r'C:\Users\Алексей\BattleCity')

from constants import RED, GREEN, BLUE
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600, 800))
background = RED

key_dict = { K_r: RED, K_g: GREEN, K_b: BLUE }

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == KEYDOWN:
            if event.key in key_dict:
                background = key_dict[event.key]
            
            caption = f'background color = {background}'
            pygame.display.set_caption(caption)
        print(event)

    screen.fill(background)
    pygame.display.update()

pygame.quit()