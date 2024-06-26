import pygame, os, csv

from TileMap.tile import Tile


class Tilemap:
    """Tilmap system"""

    def __init__(self, filename, spriteset, surface):
        self.zero_x, self.zero_y = 0, 0
        self.spriteset = spriteset
        self.tile_size = 26
        self.surface = surface

        self.load_tiles_csv(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))  
        self.load_map()
        
    def update_map(self):
        self.surface.blit(self.map_surface, (0, 0))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = list()

        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
    
        return map

    def load_tiles_csv(self, filename):
        self.map = self.read_csv(filename)
        self.load_tiles()

    def load_tiles(self):
        self.tiles = []
        self.walls = []
        self.grass = []

        x, y = 0, 0
        for row in self.map:
            x = 0
            for tile in row:
                coords = (x * self.tile_size, y * self.tile_size)
                if tile == '0':
                    tl = Tile("grass.png", coords, self.spriteset)
                    self.tiles.append(tl)
                    self.grass.append(tl)
                elif tile == '1':
                    tl = Tile("brickwall.png", coords, self.spriteset)
                    self.tiles.append(tl)
                    self.walls.append(tl)
                elif tile == '2':
                    self.tiles.append(Tile("water.png", coords, self.spriteset))
                elif tile == '3':
                    self.tiles.append(Tile("", coords, self.spriteset))

                x += 1
            y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size

    def enlarged_tilemap(self):
        pass