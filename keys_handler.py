import pygame
from pygame.locals import *

class KeysHandler:
    def __init__(self, player, bullets_handler):
        self.player = player
        self.bullets_handler = bullets_handler
        
    def check_keys(self):
        pressed_keys = pygame.key.get_pressed()

        for key in self.player.key_controls:
            if pressed_keys[K_SPACE]:
                bul = self.player.shoot()
                if bul != None:
                    self.bullets_handler.bullets.append(bul)
            if pressed_keys[key]:
                self.player.move(key)
                break