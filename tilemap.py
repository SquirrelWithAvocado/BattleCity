import pygame, tileset, numpy as np

class Tilemap:
    """Tilmap system"""

    def __init__(self, tileset, size=(10, 20), rect=None):
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)

        height, width = self.size
        self.image = pygame.Surface((32*width, 32*height))

        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()
    
    def render(self):
        m, n = self.map.shape

        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j*32, i*32))
    
    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        print(self.map)
        print(self.map.shape)
        self.render()
    
    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        print(self.map)
        self.render()
    
    def __str__(self):
        return f'{self.__class__.name} {self.size}'
