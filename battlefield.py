from pydoc import plain
import pygame
from pygame.locals import *
from player import Player

class Battlefield:
    """Game battlefield"""

    def __init__(self, screen):
        pygame.init()
        Battlefield.screen = screen
        Battlefield.running = True
        Battlefield.clock = pygame.time.Clock()
 
        Battlefield.caption = "Battlecity: battlefield"
        pygame.display.set_caption(Battlefield.caption)

        self.player = Player(screen, (640, 512))


    def run(self):
        "Battlefield event loop"
        while Battlefield.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    Battlefield.running = False
                elif event.type == KEYDOWN:
                    continue

            self.check_keys()

            Battlefield.screen.fill(Color('dark green'))
            self.player.update()
            pygame.display.update()

            Battlefield.clock.tick(30)
    
    def check_keys(self):
        self.pressed_keys = pygame.key.get_pressed()

        for key in self.player.key_controls:
            if self.pressed_keys[key]:
                self.player.move(key)
                break
