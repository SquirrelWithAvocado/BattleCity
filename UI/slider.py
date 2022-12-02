import pygame

from extra_modules.sound_config import SOUND_PARAMS


class Slider:
    def __init__(
            self,
            surface,
            position,
            slider_type,
            upper_value=1,
            width=30,
            outline_size=(300, 20)
    ):
        self.position = position
        self.slider_type = slider_type
        self.surface = surface
        self.outline_size = outline_size
        self.slider_width = width
        self.upper_value = upper_value

    def set_value(self):
        SOUND_PARAMS[self.slider_type] = self.slider_width / self.outline_size[0] / self.upper_value

    def render(self):
        self.change_value()

        pygame.draw.rect(self.surface, (0, 0, 0), (self.position[0], self.position[1],
                                                   self.outline_size[0] - 5, self.outline_size[1]), 3)

        pygame.draw.rect(self.surface, (0, 150, 0), (self.position[0] + 3, self.position[1] + 3,
                                                     self.slider_width, self.outline_size[1] - 6))

    def change_value(self):
        mouse_pos = pygame.mouse.get_pos()

        point_params = (mouse_pos[0], mouse_pos[1], self.outline_size[0],
                        self.outline_size[1], self.position[0], self.position[1])

        if self.collide_rect_point(*point_params):
            if pygame.mouse.get_pressed()[0]:
                self.slider_width = mouse_pos[0] - self.position[0]

                if self.slider_width < 1:
                    self.slider_width = 0
                if self.slider_width > self.outline_size[0] - 11:
                    self.slider_width = self.outline_size[0] - 11

        self.set_value()

    def collide_rect_point(self, px, py, rw, rh, rx, ry):
        if rx < px < rx + rw:
            if ry < py < ry + rh:
                return True
        return False
