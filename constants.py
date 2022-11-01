from pygame.locals import *

SCREEN_SIZE = (800, 900)
GAME_SURFACE_SIZE = (676, 676)
SIDE_MENU_SIZE = (676, 100)

SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE

KEYS_DICT = {
    K_s: "print('Key press S')",
    K_g: "Battlefield(self.screen).run()"
}

PLAYER_SPEED = 5

KEY_CONTROLS = {
    K_w: (0, -PLAYER_SPEED),
    K_s: (0, PLAYER_SPEED),
    K_a: (-PLAYER_SPEED, 0),
    K_d: (PLAYER_SPEED, 0),

    K_UP: (0, -PLAYER_SPEED),
    K_DOWN: (0, PLAYER_SPEED),
    K_LEFT: (-PLAYER_SPEED, 0),
    K_RIGHT: (PLAYER_SPEED, 0)
}

ROTATE_ANGLES = {
    K_w: 0,
    K_s: 180,
    K_a: 90,
    K_d: 270,

    K_UP: 0,
    K_DOWN: 180,
    K_LEFT: 90,
    K_RIGHT: 270
}

KEYS_COORDS = {
    K_w: (0, -1),
    K_s: (0, 1),
    K_a: (-1, 0),
    K_d: (1, 0),

    K_UP: (0, -1),
    K_DOWN: (0, 1),
    K_LEFT: (-1, 0),
    K_RIGHT: (1, 0)
}

GENERAL_ROTATE_ANGLES = {
    (0, -1): 0,
    (0, 1): 180,
    (-1, 0): 90,
    (1, 0): 270,
}

ENEMY_SPEED = 5

DIRECTIONS_LIST = [
    [-ENEMY_SPEED, 0],
    [ENEMY_SPEED, 0],
    [0, -ENEMY_SPEED],
    [0, ENEMY_SPEED]
]

DIRECTION_DICT = {
    0: (0, -1),
    180: (0, 1),
    90: (-1, 0),
    270: (1, 0)
}

PLAYER_RECT_SIZE = [40, 40]
PLAYER_COLOR = (0, 255, 0)

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

ARLEKIN = (68,148,74)

TILE_SIZE = 50