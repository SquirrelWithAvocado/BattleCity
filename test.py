import unittest, pygame
from battlefield import *

class TestPlayerHealth(unittest.TestCase):
    def test_fullhealth_player(self):

        start_health = 1
        battle_field = Battlefield(pygame.display.set_mode((800, 800)))
        battle_field.check_player_health()

        self.assertEqual(start_health, battle_field.player.health)
    
    def test_reincornate_dead_player(self):
        result_health = 1
        battle_field = Battlefield(pygame.display.set_mode((800, 800)))
        battle_field.player.health = 0
        battle_field.check_player_health()

        self.assertEqual(result_health, battle_field.player.health)
    
    def test_no_reincornation(self):
        result_health = 0
        battle_field = Battlefield(pygame.display.set_mode((800, 800)))
        battle_field.player.hearts = 0
        battle_field.player.health = 0
        battle_field.check_player_health()

        self.assertEqual(result_health, battle_field.player.health)


if __name__ == '__main__':
    unittest.main()