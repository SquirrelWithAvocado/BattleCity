import random
import pygame


class Bonus:
    def __init__(self, surface, player, img_path):
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.surface = surface
        self.player = player

        self.picked = False
        self.timer = 10
        self.spawn()

    def on_pick(self):
        pass

    def spawn(self):
        size = self.surface.get_rect().size
        self.rect.center = (random.randint(0, size[0]), random.randint(0, size[1]))

    def update(self):
        if not self.picked:
            self.surface.blit(self.image, self.rect)
        else:
            self.on_pick()


class SpeedBonus(Bonus):
    def __init__(self, surface, player):
        super().__init__(surface, player, r'images/bonuses/speed_bonus.png')

    def on_pick(self):
        if not self.picked:
            self.player.speed += 2
            self.picked = True
            on_pick_play()
        else:
            if self.timer <= 0:
                self.player.speed = self.player.nominal_speed
            else:
                self.timer -= 1


class HeartBonus(Bonus):
    def __init__(self, surface, player):
        super().__init__(surface, player, r'images/bonuses/heart.png')

    def on_pick(self):
        if not self.picked:
            self.player.hearts += 1
            self.picked = True
            on_pick_play()

    def update(self):
        if not self.picked:
            self.surface.blit(self.image, self.rect)


class PowerShootingBonus(Bonus):
    def __init__(self, surface, player):
        super().__init__(surface, player, r'images/bonuses/projectile.png')

    def on_pick(self):
        if not self.picked:
            self.player.super_shooting_times = 2
            self.picked = True
            on_pick_play()

    def update(self):
        if not self.picked:
            self.surface.blit(self.image, self.rect)


def on_pick_play():
    pick_sound = pygame.mixer.Sound(r'sound_effects\bonus_pick_sound.mp3')
    pick_sound.set_volume(0.3)
    pick_sound.play()
