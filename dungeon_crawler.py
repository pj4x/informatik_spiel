import random
import sys

import pygame

# add sm subfolder to path
sys.path.insert(1, "./sm/")

import sm_button
import sm_enemy
import sm_game
import sm_player
import sm_scene
import sm_text

# Initialise constants
WIDTH, HEIGHT = 800, 600
FPS = 60
MAP_SIZE = 256
TILE_SIZE = 64
name = "dungeon crawler"
running = True


##################################################################
# Initialise classes and tilemap
##################################################################

# dont actually need to provide tile size since we use standard(64), but for consistency sake
game = sm_game.sm_game(
    WIDTH, HEIGHT, name, FPS, TILE_SIZE=TILE_SIZE, cam_scroll_style=1
)


# adding scenes to main scene array
game.add_scene(sm_scene.sm_scene(game.screen, (30, 30, 30), "test", is_game_scene=True))
game.add_scene(
    sm_scene.sm_scene(game.screen, (30, 30, 30), "menu", is_game_scene=False)
)
game.add_scene(sm_scene.sm_scene(game.screen, (30, 30, 30), "inv", is_game_scene=False))
game.change_scene(1)


def btn_action(b: sm_button.sm_button):
    game.change_scene(0)


def btn_quit(b: sm_button.sm_button):
    pygame.quit()
    sys.exit()


def btn_inv(b: sm_button.sm_button):
    game.change_scene(2)


# Main menu scene
game.scenes[1].add_text(
    sm_text.sm_text(
        "Main Menu",
        310,
        10,
        pygame.font.SysFont("arial", 42),
        (255, 255, 255),
    )
)

game.scenes[1].add_button(
    sm_button.sm_button(
        400,
        100,
        200,
        100,
        "Play",
        (32, 220, 35),
        pygame.font.SysFont("arial", 42),
        (0, 0, 0),
        btn_action,
    )
)
game.scenes[1].add_button(
    sm_button.sm_button(
        400,
        100,
        200,
        250,
        "Inventory",
        (100, 0, 0),
        pygame.font.SysFont("arial", 42),
        (0, 0, 0),
        btn_inv,
    )
)
game.scenes[1].add_button(
    sm_button.sm_button(
        400,
        100,
        200,
        400,
        "Quit Game",
        (136, 136, 255),
        pygame.font.SysFont("arial", 42),
        (0, 0, 0),
        btn_quit,
    )
)


# test scene
game.scenes[0].add_player(
    sm_player.sm_player(
        (256 * 64) // 2,
        (256 * 64) // 2,
        6,
        "textures/sprites/player.png",
    )
)


# Start with all walls
tilemap = [[1 for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]


def carve_block(x, y):
    """Carve a 2x2 path block"""
    for dy in (0, 1):
        for dx in (0, 1):
            if 0 <= x + dx < MAP_SIZE and 0 <= y + dy < MAP_SIZE:
                tilemap[y + dy][x + dx] = 0


def generate_maze():
    stack = []

    start_x = random.randrange(1, MAP_SIZE - 2, 4)
    start_y = random.randrange(1, MAP_SIZE - 2, 4)

    carve_block(start_x, start_y)
    stack.append((start_x, start_y))

    while stack:
        x, y = stack[-1]

        directions = [(4, 0), (-4, 0), (0, 4), (0, -4)]
        random.shuffle(directions)

        carved = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 1 <= nx < MAP_SIZE - 2 and 1 <= ny < MAP_SIZE - 2:
                if tilemap[ny][nx] == 1:
                    # carve corridor
                    carve_block(x + dx // 2, y + dy // 2)
                    carve_block(nx, ny)
                    stack.append((nx, ny))
                    carved = True
                    break

        if not carved:
            stack.pop()


generate_maze()
for y in range(127, 130):
    for x in range(127, 130):
        tilemap[y][x] = 0


tiles = [
    pygame.image.load("textures/map/brick_wall.png").convert_alpha(),  # 1
]

# Ensure correct size
tiles = [pygame.transform.scale(t, (TILE_SIZE, TILE_SIZE)) for t in tiles]

# tiles with collision
collides = [1]

game.scenes[0].add_map(tilemap, tiles, collides)


# inventory scene
game.scenes[2].add_text(
    sm_text.sm_text(
        "Inventory",
        300,
        5,
        pygame.font.SysFont("arial", 42),
        (255, 255, 255),
    )
)


game.scenes[2].add_text(
    sm_text.sm_text(
        "Storage",
        535,
        40,
        pygame.font.SysFont("arial", 24),
        (255, 255, 255),
    )
)

game.scenes[2].add_text(
    sm_text.sm_text(
        "Player Equipement",
        40,
        40,
        pygame.font.SysFont("arial", 24),
        (255, 255, 255),
    )
)


# inventory storage
for i in range(6):
    for j in range(7):
        game.scenes[2].add_button(
            sm_button.sm_button(
                50,
                50,
                380 + (i * 70),
                80 + (j * 70),
                "",
                (105, 105, 105),
                pygame.font.SysFont("arial", 42),
                (0, 0, 0),
                btn_action,
            )
        )


# two ability slots
for i in range(2):
    game.scenes[2].add_button(
        sm_button.sm_button(
            50,
            50,
            250,
            80 + (i * 70),
            "",
            (105, 105, 105),
            pygame.font.SysFont("arial", 42),
            (0, 0, 0),
            btn_action,
        )
    )

# four weapon slots
for i in range(4):
    game.scenes[2].add_button(
        sm_button.sm_button(
            50,
            50,
            40 + (i * 70),
            360,
            "",
            (105, 105, 105),
            pygame.font.SysFont("arial", 42),
            (0, 0, 0),
            btn_action,
        )
    )

# player icon
game.scenes[2].add_button(
    sm_button.sm_button(
        190,
        260,
        40,
        80,
        "Picture from player",
        (105, 105, 105),
        pygame.font.SysFont("arial", 24),
        (0, 0, 0),
        btn_action,
    )
)


##################################################################
#
##################################################################
