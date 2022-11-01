import pygame
from pygame.locals import *
from battlefield import Battlefield
from text import Text
from constants import SCREEN_SIZE, KEYS_DICT


class Game:
    """Single-window with multiple scenes."""

    def __init__(self):
        pygame.init()

        self.set_decor()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.running = True

        self.load_background()

    def set_decor(self):
        self.caption = "Battlecity: menu"
        self.icon = pygame.image.load(r'images\icon.png')

        pygame.display.set_caption(self.caption)
        pygame.display.set_icon(self.icon)

    def load_background(self):
        self.image = pygame.image.load(r'images\skinner.png').convert()
        self.image = pygame.transform.scale(self.image, SCREEN_SIZE)

    def run(self):
        """Main event loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                if event.type == KEYDOWN:
                    if event.key in KEYS_DICT:
                        self.do_shortcut(event)

                self.screen.blit(self.image, self.screen.get_rect())

                self.type_text(
                    "Press 'g' to go on Battlefield",
                    (self.screen.get_rect().right / 2, self.screen.get_rect().bottom / 2)
                )

                pygame.display.update()
                self.clock.tick(30)

        pygame.quit()

    def type_text(self, text, coord):
        text = Text(text, coord, fontsize=64, color='white')
        text.draw(self.screen)

    def do_shortcut(self, event):
        """Execute combination"""
        k = event.key

        if k in KEYS_DICT:
            exec(KEYS_DICT[k])
