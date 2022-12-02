import unittest
import pygame.event

from TileMap import Spriteset
from battlefield import Battlefield
from game_objects.bullet import Bullet
from game_objects.creatures import Creature


def calculate_pos(obj):
    x, y = obj.rect.topleft
    return x // 26, y // 26


class BattleFieldLoadTestCase(unittest.TestCase):
    def setUp(self):
        self.screen = pygame.display.set_mode([1, 1], flags=pygame.NOFRAME)
        self.battlefield = Battlefield(self.screen, 'test')

    def test_json_equality2tile_map_dict(self):
        for sprite in self.battlefield.tile_map_layer_one.tiles_dict.keys():
            self.assertTrue(Spriteset(r'TileMap\spriteset.png').parse_sprite(sprite + '.png'))

    def test_player_pos(self):
        self.assertEqual((13, 10), calculate_pos(self.battlefield.player))

    def test_eagle_pos(self):
        self.assertEqual((13, 12), calculate_pos(self.battlefield.eagle))

    def test_enemy_pos(self):
        self.battlefield.spawn_enemy()
        self.battlefield.respawn_timer = self.battlefield.enemy_respawn_time
        self.battlefield.spawn_enemy()

        enemy_one = self.battlefield.enemies[0]
        enemy_two = self.battlefield.enemies[1]

        self.assertEqual((9, 8), calculate_pos(enemy_one))
        self.assertEqual((17, 8), calculate_pos(enemy_two))

    def test_loaded_grass_tiles(self):
        grass_len = 76
        self.assertEqual(
            grass_len,
            len(self.battlefield.tile_map_layer_one.tiles_dict['grass']),
            f'grass tiles number should be: {grass_len}'
        )

    def test_loaded_walls_tiles(self):
        walls_len = 44
        self.assertEqual(
            walls_len,
            len(self.battlefield.tile_map_layer_one.tiles_dict['walls']),
            f'walls tiles number should be: {walls_len}'
        )

    def test_loaded_water_tiles(self):
        water_len = 556
        self.assertEqual(
            water_len,
            len(self.battlefield.tile_map_layer_one.tiles_dict['water']),
            f'walls tiles number should be: {water_len}'
        )


class BattleFieldFlagsUpdateTestCase(unittest.TestCase):
    def setUp(self):
        self.screen = pygame.display.set_mode([1, 1], flags=pygame.NOFRAME)
        self.battlefield = Battlefield(self.screen, 'test')

    def test_game_over_with_shot_player(self):
        self.battlefield.player.is_alive = False
        self.battlefield.update_game_over()

        self.assertTrue(self.battlefield.game_over)

    def test_game_over_with_shot_eagle(self):
        self.battlefield.eagle.is_alive = False
        self.battlefield.update_game_over()

        self.assertTrue(self.battlefield.game_over)

    def test_game_win(self):
        self.battlefield.enemy_limit = 0
        self.battlefield.update_objects()

        self.assertTrue(self.battlefield.game_win)


class BattleFieldGameObjectsStatusTestCase(unittest.TestCase):
    def setUp(self):
        self.screen = pygame.display.set_mode([1, 1], flags=pygame.NOFRAME)
        self.battlefield = Battlefield(self.screen, 'test')

    def test_bullets_start_num(self):
        self.assertEqual(0, len(self.battlefield.bullets))

    def test_bullets_addition(self):
        bullets_len_before = len(self.battlefield.bullets)
        self.battlefield.update_objects()

        self.assertEqual(bullets_len_before + 1, len(self.battlefield.bullets))

    def test_bonus_spawn(self):
        bonus_expected_num = 1
        self.battlefield.update_objects()
        self.battlefield.spawn_enemy()
        self.battlefield.enemies[len(self.battlefield.enemies) - 1].is_alive = False
        self.battlefield.update_objects()

        self.assertEqual(bonus_expected_num, len(self.battlefield.bonuses))

    def test_limited_enemy_spawn(self):
        expected_num = 10
        for i in range(100):
            self.battlefield.spawn_enemy()
            self.battlefield.respawn_timer = self.battlefield.enemy_respawn_time
        self.battlefield.update_objects()

        self.assertEqual(expected_num, len(self.battlefield.enemies))

    def test_limit_degrade(self):
        old_limit = self.battlefield.enemy_limit
        self.battlefield.spawn_enemy()
        self.battlefield.update_objects()

        self.assertLess(self.battlefield.enemy_limit, old_limit)


class CreatureParamsTestCase(unittest.TestCase):
    def setUp(self):
        self.screen = pygame.display.set_mode([1, 1], flags=pygame.NOFRAME)
        self.battlefield = Battlefield(self.screen, 1)
        self.creature = Creature(
            1,
            'Creature',
            self.screen,
            (0, 0),
            self.battlefield.tile_map_layer_one,
            r'images\UI images\icon.jpg',
            1,
            1
        )

    def test_alive_creature(self):
        self.assertTrue(self.creature.is_alive)

    def test_creature_rotation(self):
        self.creature.rotate(180)
        self.assertEqual(self.creature.angle, 180)

    def test_no_tile_collision(self):
        self.assertFalse(self.creature.check_tile_collision())

    def test_screen_border_collision(self):
        self.assertTrue(self.creature.check_screen_border())

    def test_bullet_dir180(self):
        self.creature.rect.center = (50, 50)
        self.creature.update()

        self.creature.rotate(180)
        self.creature.process_bullet_dir()
        self.assertEqual(self.creature.px1, 42)
        self.assertEqual(self.creature.px2, 55)
        self.assertEqual(self.creature.py1, 70)
        self.assertEqual(self.creature.py2, 70)

    def test_bullet_dir270(self):
        self.creature.rect.center = (50, 50)
        self.creature.update()

        self.creature.rotate(180)
        self.creature.rotate(270)
        self.creature.process_bullet_dir()
        self.assertEqual(self.creature.px1, 70)
        self.assertEqual(self.creature.px2, 70)
        self.assertEqual(self.creature.py1, 42)
        self.assertEqual(self.creature.py2, 55)


class PlayerFunctionalityTestCase(unittest.TestCase):
    def setUp(self):
        self.screen = pygame.display.set_mode([1, 1], flags=pygame.NOFRAME)
        self.battlefield = Battlefield(self.screen, 1)

    def test_full_health_player(self):
        start_health = 1
        self.assertEqual(start_health, self.battlefield.player.health)

    def test_respawn_shot_player(self):
        self.battlefield = Battlefield(self.screen, 1)
        result_health = 1
        self.battlefield.player.health = 0
        self.battlefield.player.hearts = 1

        self.battlefield.player.update()

        self.assertEqual(result_health, self.battlefield.player.health)

    def test_shot_player(self):
        result_health = 0
        self.battlefield = Battlefield(self.screen, 1)
        self.battlefield.player.hearts = 0
        self.battlefield.player.health = 0

        self.battlefield.player.update()

        self.assertEqual(result_health, self.battlefield.player.health)

    def test_player_bonus_on_pick(self):
        self.battlefield.spawn_bonus()
        self.battlefield.bonuses[0].rect.topleft = self.battlefield.player.rect.topleft

        self.battlefield.update_objects()
        self.battlefield.bonuses[0].on_pick()

        self.assertTrue(self.battlefield.bonuses[0].picked)

    def test_point_count(self):
        self.battlefield.spawn_enemy()
        self.battlefield.update_objects()

        self.battlefield.enemies[0].is_alive = False

        self.battlefield.update_objects()

        self.assertGreater(self.battlefield.player.score, 0)


class EnemyFunctionalityTestCase(unittest.TestCase):
    def setUp(self):
        self.screen = pygame.display.set_mode([1, 1], flags=pygame.NOFRAME)
        self.battlefield = Battlefield(self.screen, 1)
        self.battlefield.enemy_types[0] = 0
        self.battlefield.update_objects()
        self.enemy = self.battlefield.enemies[0]
        self.battlefield.update_objects()

    def test_enemy_is_alive(self):
        self.assertTrue(self.enemy.is_alive)

    def test_enemy_class_spawn(self):
        self.assertEqual(self.enemy.enemy_type, 0)

    def test_enemy_id(self):
        for i in range(5):
            self.battlefield.respawn_timer = self.battlefield.enemy_respawn_time
            self.battlefield.spawn_enemy()

        self.assertEqual(5, self.battlefield.enemies[len(self.battlefield.enemies) - 1].id)

    def test_shooting(self):
        bullets_len = len(self.battlefield.bullets)
        self.enemy.shoot()

        self.assertEqual(bullets_len + 1, len(self.battlefield.bullets))

    def test_invert_directions(self):
        old_direction = self.enemy.direction
        self.enemy.invert_direction()

        self.assertEqual([-old_direction[0], -old_direction[1]], self.enemy.direction)

    def test_another_enemy_collision(self):
        self.battlefield.respawn_timer = self.battlefield.enemy_respawn_time
        self.battlefield.spawn_enemy()
        self.battlefield.update_objects()

        self.battlefield.update_objects()

        self.assertFalse(self.enemy.check_another_enemy_collision())

    def test_move_to(self):
        self.enemy.move_to(self.battlefield.player)

        self.assertEqual([0, 1], self.enemy.direction)

    def test_move_to_on_first_period(self):
        self.enemy.cur_time = 0
        self.enemy.change_direction()

        self.assertTrue(self.enemy.direction)

    def test_move_to_on_second_period(self):
        self.enemy.cur_time = self.enemy.period * 1.5
        self.enemy.change_direction()

        self.assertTrue([0, 0], self.enemy.direction)

    def test_move_to_on_third_period(self):
        self.enemy.cur_time = self.enemy.period * 2 + 1
        self.enemy.change_direction()

        self.assertTrue([0, 0], self.enemy.direction)


class BonusesFunctionalityTestCase(unittest.TestCase):
    def setUp(self):
        self.screen = pygame.display.set_mode([1, 1], flags=pygame.NOFRAME)
        self.battlefield = Battlefield(self.screen, 1)

    def test_bonus_spawn(self):
        self.battlefield.respawn_timer = self.battlefield.enemy_respawn_time
        self.battlefield.spawn_enemy()
        self.battlefield.update_objects()

        self.battlefield.enemies[0].is_alive = False
        self.battlefield.update_objects()

        self.assertEqual(1, len(self.battlefield.bonuses))

    def test_bonus_on_pick(self):
        self.battlefield.spawn_bonus()
        self.battlefield.update_objects()

        self.battlefield.bonuses[0].on_pick()

        self.assertTrue(self.battlefield.bonuses[0].picked)

    def test_power_shooting_bonus(self):
        self.battlefield.enemy_limit = 10
        self.battlefield.spawn_enemy()
        self.battlefield.update_objects()

        self.battlefield.spawn_bonus()
        self.battlefield.bonuses[0].on_pick()

        self.assertEqual(2, self.battlefield.player.super_shooting_times)

    def test_heart_bonus(self):
        old_hearts_num = self.battlefield.player.hearts

        self.battlefield.enemy_limit = 10
        self.battlefield.spawn_enemy()
        self.battlefield.respawn_timer = self.battlefield.enemy_respawn_time
        self.battlefield.spawn_enemy()
        self.battlefield.update_objects()

        self.battlefield.spawn_bonus()
        self.battlefield.bonuses[0].on_pick()
        self.battlefield.update_objects()

        self.assertEqual(old_hearts_num + 1, self.battlefield.player.hearts)

    def test_speed_bonus(self):
        self.battlefield.enemy_limit = 10
        self.battlefield.spawn_enemy()
        self.battlefield.respawn_timer = self.battlefield.enemy_respawn_time
        self.battlefield.spawn_enemy()
        self.battlefield.respawn_timer = self.battlefield.enemy_respawn_time
        self.battlefield.spawn_enemy()
        self.battlefield.update_objects()

        self.battlefield.spawn_bonus()
        self.battlefield.bonuses[0].on_pick()
        self.battlefield.update_objects()

        self.assertEqual(7, self.battlefield.player.speed)


class BulletFunctionalityTestCase(unittest.TestCase):
    def setUp(self):
        self.screen = pygame.display.set_mode([1, 1], flags=pygame.NOFRAME)
        self.battlefield = Battlefield(self.screen, 1)

    def test_bullet_alive_on_collision(self):
        self.battlefield.update_objects()
        self.battlefield.bullets[0].is_alive = False
        self.battlefield.update_objects()
        self.assertEqual(1, len(self.battlefield.bullets))

    def test_bullet_collision_on_creature(self):
        self.battlefield.update_objects()
        creature = Creature(
            1,
            'Enemy',
            self.screen,
            (0, 0),
            self.battlefield.tile_map_layer_one,
            r'images\player animation\animation_go.png',
            1,
            1
        )

        bullet = Bullet(
            self.battlefield.enemies[0],
            (0, 0),
            [0, 1],
            1,
            self.screen,
            self.battlefield.tile_map_layer_one,
            self.battlefield.enemies,
            creature,
            self.battlefield.eagle,
            False
        )
        self.battlefield.update_objects()
        self.assertTrue(bullet.is_alive)


if __name__ == '__main__':
    unittest.main()
