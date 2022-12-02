import sys

import pygame
from pygame.locals import *

from UI import Cursor
from battlefield import Battlefield
from UI.button import Button
from UI.mouse_handler import MouseHandler
from UI.text import Text
from extra_modules.sound_config import SOUND_PARAMS
from extra_modules.constants import SCREEN_SIZE, KEYS_DICT, MENU_BUTTON_SIZE
from settings_menu import SettingsMenu


class Game:
    """Single-window with multiple scenes."""

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.running = True

        self.cursor = Cursor()
        self.holes = []

        pygame.mixer.music.load(r'sound_effects\main theme.mp3')

        self.load_background()
        self.set_decor()
        self.buttons_list = []
        self.mouse_handler = MouseHandler(self.buttons_list, self.screen, self.holes)

        self.image = self.load_background()

        self.construct_buttons()

    def construct_buttons(self):
        self.buttons_list.append(
            Button(
                (SCREEN_SIZE[0] // 2 - 100, SCREEN_SIZE[1] // 2 - 200),
                MENU_BUTTON_SIZE,
                "Play",
                on_click=lambda x: Battlefield(self.screen, 1).run()
            )
        )

        self.buttons_list.append(
            Button(
                (SCREEN_SIZE[0] // 2 - 100, SCREEN_SIZE[1] // 2 - 200 + 120),
                MENU_BUTTON_SIZE,
                "Settings",
                on_click=lambda x: SettingsMenu(self.screen, self.image, self.cursor).run()
            )
        )

        self.buttons_list.append(
            Button(
                (SCREEN_SIZE[0] // 2 - 100, SCREEN_SIZE[1] // 2 - 200 + 240),
                MENU_BUTTON_SIZE,
                "Quit",
                on_click=lambda x: sys.exit()
            )
        )

    def set_decor(self):
        caption = "Battlecity: menu"
        icon = pygame.image.load(r'images\UI images\icon.png').convert_alpha()

        pygame.display.set_caption(caption)
        pygame.display.set_icon(icon)

    def load_background(self):
        image = pygame.image.load(r'images\UI images\tank_background_1.png').convert_alpha()
        image = pygame.transform.scale(image, SCREEN_SIZE)

        return image

    def run(self):
        """Main event loop."""
        pygame.mixer.music.set_volume(min(SOUND_PARAMS['general'], SOUND_PARAMS['music']))
        pygame.mixer.music.play(-1)
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                if event.type == KEYDOWN:
                    if event.key in KEYS_DICT:
                        self.do_shortcut(event)

                self.mouse_handler.mouse_event(event.type, pygame.mouse.get_pos())

            self.screen.blit(self.image, self.screen.get_rect())

            self.draw_ui()

            pygame.display.update()

        pygame.quit()

    def draw_ui(self):
        for button in self.buttons_list:
            if button.is_active:
                button.draw(self.screen)

        for hole in self.holes:
            hole.draw()

        self.cursor.update(pygame.mouse.get_pos(), self.screen)

    def type_text(self, text, coord):
        text = Text(text, coord, fontsize=64, color='white')
        text.draw(self.screen)

    def do_shortcut(self, event):
        """Execute combination"""
        k = event.key

        if k in KEYS_DICT:
            exec(KEYS_DICT[k])
