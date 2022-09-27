import pygame

class Tileset:
    """Tileset system"""

    def __init__(self, file, size=(32, 32), field=1, spacing=1):
        self.file = file
        self.size = size
        self.field = field
        self.spacing = spacing
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()
    
    def load(self):

        self.tiles = []
        x0 = y0 = self.field
        width, height = self.rect.size

        dx = self.size[0] + self.spacing 
        dy = self.size[1] + self.spacing

        for x in range(x0, width, dx):
            for y in range(y0, height, dy):
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)
    
    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'