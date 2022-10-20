import pygame, random
from pygame.locals import *
from TileMap import tilemap
from creatures.player import Player
from creatures.enemy import Enemy, EnemyType
from creatures.eagle import Eagle
from TileMap import *
from text import Text

from battlefield_interfaces import SideInterface
from keys_handler import KeysHandler
from enemies_handler import EnemiesHandler
from bullets_handler import BulletsHandler

class Battlefield:
    """Game battlefield"""

    def __init__(self, screen, level, players_num):
        pygame.init()
        self.caption = "Battlecity: battlefield"
        pygame.display.set_caption(self.caption)
        self.screen = screen

        self.surface_size = (676, 676)
        self.game_surface = pygame.Surface(self.surface_size)

        self.running = True
        self.clock = pygame.time.Clock()

        self.level = level
        self.player_count = players_num

        self.spriteset = Spriteset(r'TileMap\spriteset1.png')
        self.load_map(self.level)
        self.side_menu = SideInterface(screen)

        
        self.enemies_handler = EnemiesHandler(self.player, self.eagle, self.game_surface, 10, self.level, self.tilemap) 
        self.bullets_handler = BulletsHandler(self.enemies_handler.enemies, self.player)
        self.keys_handler = KeysHandler(self.player, self.bullets_handler)

    def load_map(self, level):
        self.tilemap = Tilemap(fr'TileMap\maps\map_{self.level}.csv', self.spriteset, self.game_surface)
        self.eagle = Eagle(self.game_surface, (338, 651))
        self.bullets = []
        
        self.player_point = (320, 550)
        self.player = Player(self.game_surface, self.player_point, self.tilemap)
        
        self.running = True

        self.level = level
        if self.level != 1:
            self.run()

    def run(self):
        "Battlefield event loop"
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    continue

            self.keys_handler.check_keys()
            self.update_interfaces()
            self.update_game_objects()
                                                 
            self.respawn_timer += 1     
            pygame.display.update()

            self.clock.tick(30)
        
        if not(self.player.is_alive) and self.player.hearts == 0 or not(self.eagle.is_alive):
            self.load_map(self.level)
    
    def update_interfaces(self):
        self.screen.fill(Color('gray'))
        self.produce_end_text()
        self.screen.blit(self.game_surface, (50, 50))
        self.side_menu.update()

    def update_game_objects(self):
        self.restart_game()

        self.tilemap.update_map()
        if self.eagle.is_alive:
                self.eagle.update()  
        self.player.update()
        self.enemies_handler.update_enemies()
        self.bullets_handler.update_bullets()
    
    def restart_game(self):
        player_dead = not(self.player.is_alive)
        zero_hearts = self.player.hearts == 0
        eagle_dead = not(self.eagle.is_alive)
        space_pressed = pygame.key.get_pressed()[K_SPACE]

        if ((player_dead and zero_hearts or eagle_dead) and space_pressed):
                self.running = False

    def produce_end_text(self):
            if not(self.player.is_alive) and self.player.hearts == 0 or not(self.eagle.is_alive):
                Text("GAME OVER", (338, 338), fontsize=64, color='white').draw(self.game_surface)
                Text("Press space to restart", (338, 378), fontsize=32, color='white').draw(self.game_surface)
            if len(self.enemies_handler.enemies) == 0 and self.enemies_handler.enemy_limit == 0:
                Text("YOU WIN", (338, 338), fontsize=64, color='white').draw(self.game_surface)
                Text("Press space to go next level", (328, 378), fontsize=32, color='white').draw(self.game_surface)

