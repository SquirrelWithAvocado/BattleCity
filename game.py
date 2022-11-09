import sys

import pygame
from pygame.locals import *
from battlefield import Battlefield
from UI.button import Button
from mouse_handler import MouseHandler
from UI.text import Text
from constants import SCREEN_SIZE, KEYS_DICT, MENU_BUTTON_SIZE


class Game:
    """Single-window with multiple scenes."""

    def __init__(self):
        pygame.init()

        self.set_decor()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.running = True

        self.image = self.load_background()

        self.buttons_list = []
        self.construct_buttons()

        self.mouse_handler = MouseHandler(self.buttons_list, self.screen)

        self.load_background()

    def construct_buttons(self):
        self.buttons_list.append(
            Button(
                (SCREEN_SIZE[0] // 2 - 100, SCREEN_SIZE[1] // 2 - 100),
                MENU_BUTTON_SIZE,
                "Play",
                on_click=lambda x: Battlefield(self.screen).run()
            )
        )
        self.buttons_list.append(
            Button(
                (SCREEN_SIZE[0] // 2 - 100, SCREEN_SIZE[1] // 2 - 100 + 60),
                MENU_BUTTON_SIZE,
                "Settings"
            )
        )
        self.buttons_list.append(
            Button(
                (SCREEN_SIZE[0] // 2 - 100, SCREEN_SIZE[1] // 2 - 100 + 120),
                MENU_BUTTON_SIZE,
                "Quit",
                on_click=lambda x: sys.exit()
            )
        )

    def set_decor(self):
        caption = "Battlecity: menu"
        icon = pygame.image.load(r'images\icon.png')

        pygame.display.set_caption(caption)
        pygame.display.set_icon(icon)

    def load_background(self):
        image = pygame.image.load(r'images\tank_background_1.png').convert_alpha()
        image = pygame.transform.scale(image, SCREEN_SIZE)

        return image

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

                for button in self.buttons_list:
                    button.draw(self.screen)

                self.mouse_handler.mouse_event(event.type, pygame.mouse.get_pos())

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
