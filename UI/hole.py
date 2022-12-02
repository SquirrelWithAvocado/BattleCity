import pygame

from extra_modules.sound_config import SOUND_PARAMS


class Hole:
    def __init__(self, pos, surface):
        big_image = pygame.image.load(r'images/UI images/bullet_hole.png').convert_alpha()

        self.image = pygame.transform.scale(big_image, (40, 40))
        self.pos = pos
        self.surface = surface
        self.shift = -20

        self.play_sound_effects()

    def play_sound_effects(self):
        shoot_sound = pygame.mixer.Sound(r'sound_effects\shot_message_2.mp3')
        shoot_sound.set_volume(SOUND_PARAMS['effects'])

        shoot_sound.play()

    def draw(self):
        self.surface.blit(self.image, (self.pos[0] + self.shift, self.pos[1] + self.shift))
