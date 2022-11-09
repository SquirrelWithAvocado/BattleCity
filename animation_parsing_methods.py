import json

import pygame


def parse_animation(filepath):
    file = filepath.replace('png', 'json')
    frames = []
    big_image = pygame.image.load(filepath)
    with open(file) as f:
        meta_data = json.load(f)

    for data_el in meta_data['frames']:
        x, y, width, height = data_el["x"], data_el["y"], data_el["width"], data_el["height"]
        frames.append(get_sprite(x, y, width, height, big_image))
    return frames


def get_sprite(x, y, width, height, big_image):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(big_image, (0, 0), (x, y, width, height))
    return sprite