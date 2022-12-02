import pygame

from pygame import QUIT
from UI import Button, MouseHandler, Text
from UI.slider import Slider
from extra_modules.sound_config import SOUND_PARAMS
from extra_modules.constants import SCREEN_SIZE


class SettingsMenu:
    def __init__(self, screen, background, cursor):
        self.screen = screen
        self.background = background
        self.running = True

        self.go_back_button = Button((350, 600), (130, 50), 'Go back', on_click=lambda x: self.set_running_false())

        self.sliders = []
        self.txts = []

        self.construct_sliders()
        self.construct_txts()
        self.mouse_handler = MouseHandler([self.go_back_button], self.screen, [])
        self.cursor = cursor

    def construct_sliders(self):
        self.sliders.append(Slider(self.screen, (SCREEN_SIZE[0] // 2 - 135, SCREEN_SIZE[1] // 2 - 160), 'general'))
        self.sliders.append(Slider(self.screen, (SCREEN_SIZE[0] // 2 - 135, SCREEN_SIZE[1] // 2 - 80), 'music'))
        self.sliders.append(Slider(self.screen, (SCREEN_SIZE[0] // 2 - 135, SCREEN_SIZE[1] // 2 + 20), 'effects'))

    def construct_txts(self):
        self.txts.append(Text(
            "General volume",
            (SCREEN_SIZE[0] // 2 + 10, SCREEN_SIZE[1] // 2 - 170),
            fontsize=36)
        )

        self.txts.append(Text(
            "Music volume",
            (SCREEN_SIZE[0] // 2 + 10, SCREEN_SIZE[1] // 2 - 90),
            fontsize=36)
        )

        self.txts.append(Text(
            "Effects volume",
            (SCREEN_SIZE[0] // 2 + 10, SCREEN_SIZE[1] // 2 + 10),
            fontsize=36)
        )

    def set_running_false(self):
        self.running = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                self.mouse_handler.mouse_event(event.type, pygame.mouse.get_pos())
            self.screen.blit(self.background, self.screen.get_rect())

            for hole in self.mouse_handler.holes:
                hole.draw()

            self.update_sliders()

            self.go_back_button.draw(self.screen)

            self.update_txts()
            self.cursor.update(pygame.mouse.get_pos(), self.screen)
            self.update_settings()
            pygame.display.update()

        self.mouse_handler.buttons.pop()

    def update_settings(self):
        pygame.mixer.music.set_volume(min(SOUND_PARAMS['general'], SOUND_PARAMS['music']))

    def update_sliders(self):
        for slider in self.sliders:
            slider.render()

    def update_txts(self):
        for txt in self.txts:
            txt.draw(self.screen)
