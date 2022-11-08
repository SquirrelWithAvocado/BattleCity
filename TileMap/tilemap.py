import pygame, os, csv
from TileMap.tile import Tile
from TileMap.spriteset import Spriteset


class Tilemap:
    """Tilmap system"""

    def __init__(self, level, surface):
        self.zero_x, self.zero_y = 0, 0
        self.spriteset = Spriteset(r'TileMap\spriteset.png')
        self.tile_size = 26
        self.surface = surface
        self.enemy_spawns = []
        self.hero_spawn = (0, 0)

        self.load_tiles_csv(fr'TileMap\maps\map_{level}.csv')
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def get_all_tiles(self):
        result = list()
        for tile_list in self.tiles_dict.values():
            for tile in tile_list:
                result.append(tile)
        self.tiles = result

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
        self.tiles_dict = {'walls': [], 'grass': [], 'water': []}

        x, y = 0, 0
        for row in self.map:
            x = 0
            for tile in row:
                coords = (x * self.tile_size, y * self.tile_size)
                if tile == '0':
                    self.tiles_dict['grass'].append(Tile("grass.png", coords, self.spriteset))
                elif tile == '1':
                    self.tiles_dict['walls'].append(Tile("brickwall.png", coords, self.spriteset))
                elif tile == '2':
                    self.tiles_dict['water'].append(Tile("water.png", coords, self.spriteset))
                elif tile == '3':
                    self.enemy_spawns.append(coords)
                    self.tiles_dict['grass'].append(Tile("grass.png", coords, self.spriteset))
                elif tile == '4':
                    self.hero_spawn = coords
                    self.tiles_dict['grass'].append(Tile("grass.png", coords, self.spriteset))
                elif tile == '5':
                    self.eagle_spawn = coords
                    self.tiles_dict['grass'].append(Tile("grass.png", coords, self.spriteset))
                x += 1
            y += 1

        self.get_all_tiles()
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size

    def get_enemy_spawns(self):
        return self.enemy_spawns.copy()

    def get_player_spawn(self):
        return self.hero_spawn

    def get_eagle_spawn(self):
        return self.eagle_spawn

    def update(self):
        self.surface.blit(self.map_surface, (0, 0))
