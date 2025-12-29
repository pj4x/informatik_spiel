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

# generate tilemap with checkerboard pattern
tilemap = [[(x + y) % 2 for x in range(MAP_SIZE)] for y in range(MAP_SIZE)]

tiles = [
    pygame.image.load("textures/map/brick_wall.png").convert_alpha(),  # 1
]

# Ensure correct size
tiles = [pygame.transform.scale(t, (TILE_SIZE, TILE_SIZE)) for t in tiles]

game.scenes[0].add_map(tilemap, tiles)


# inventory scene
game.scenes[2].add_text(
    sm_text.sm_text(
        "Inventory",
        310,
        10,
        pygame.font.SysFont("arial", 42),
        (255, 255, 255),
    )
)


##################################################################
#
##################################################################
