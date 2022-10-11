import pygame, json

class Spriteset:
    def __init__(self, file_path):
        self.file_path = file_path
        self.sprite_sheet = pygame.image.load(file_path).convert()
        self.meta_data = self.file_path.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, width, height))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]
        x, y, width, height = sprite["x"], sprite["y"], sprite["width"], sprite["height"]
        image = self.get_sprite(x, y, width, height)
        return image