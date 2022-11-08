import pygame


class Bullet:
    def __init__(self, parent, px, py, direction, damage, surface, tile_map, enemies, player, eagle):
        self.surface = surface
        self.surface_size = surface.get_size()
        self.parent = parent
        self.tile_map = tile_map
        self.image = pygame.image.load(r'images\bullet1.png')
        self.rect = self.image.get_rect()
        self.is_alive = True
        self.enemies = enemies
        self.player = player
        self.eagle = eagle

        self.rect.center = (px, py)
        self.damage = damage
        self.dx, self.dy = direction[0], direction[1]
        self.direction = [direction[0], direction[1]]

        self.speed = 10

        self.angle_dict = {
            (-1, 0): 90,
            (1, 0): -90,
            (0, -1): 0,
            (0, 1): 180
        }

        self.rotate()

    def update(self):
        self.move_bullet()
        self.check_surface_border()
        self.surface.blit(self.image, self.rect)
        self.check_collisions()

    def check_collisions(self):
        self.check_tile_collision()
        if self.parent.name == "Player":
            self.check_enemy_collision()
        if self.parent.name == "Enemy":
            self.check_player_collision()

    def move_bullet(self):
        self.rect.move_ip(self.dx * self.speed, self.dy * self.speed)

    def check_tile_collision(self):
        for tile in self.tile_map.tiles:
            if tile.name == 'brickwall' and self.rect.colliderect(
                    tile.rect) and tile in self.tile_map.tiles:
                self.tile_map.tiles.remove(tile)
                self.is_alive = False
                x, y = tile.rect.topleft[1] // 26, tile.rect.topleft[0] // 26
                self.tile_map.map[x][y] = '0'
                self.tile_map.load_tiles()
                self.tile_map.load_map()

    def check_enemy_collision(self):
        for enemy in self.enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.health -= self.damage
                self.is_alive = False

    def check_player_collision(self):
        if self.rect.colliderect(self.player.rect):
            self.player.health -= 1
            self.is_alive = False
        if self.rect.colliderect(self.eagle.rect):
            self.eagle.health -= 1
            self.is_alive = False

    def check_surface_border(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.is_alive = False
        if self.rect.right > self.surface_size[0]:
            self.rect.right = self.surface_size[0]
            self.is_alive = False
        if self.rect.top <= 0:
            self.rect.top = 0
            self.is_alive = False
        if self.rect.bottom >= self.surface_size[1]:
            self.rect.bottom = self.surface_size[1]
            self.is_alive = False

    def rotate(self):
        self.normalize_direction()
        self.image = pygame.transform.rotate(self.image, self.angle_dict[(self.direction[0], self.direction[1])])
        self.rect = self.image.get_rect(center=self.rect.center)

    def normalize_direction(self):
        if self.direction[0] != 0:
            self.direction[0] = self.direction[0] // abs(self.direction[0])
        if self.direction[1] != 0:
            self.direction[1] = self.direction[1] // abs(self.direction[1])
