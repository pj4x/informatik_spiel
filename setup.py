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
name = "dungeon crawler"
running = True

##################################################################
# Initialise classes
##################################################################
game = sm_game.sm_game(WIDTH, HEIGHT, name, FPS)


# adding scenes to main scene array
test_scene = sm_scene.sm_scene(game.screen, (30, 30, 30), is_game_scene=True)
game.add_scene(test_scene)
menu_scene = sm_scene.sm_scene(game.screen, (30, 30, 30), is_game_scene=False)
game.add_scene(menu_scene)
inv_scene = sm_scene.sm_scene(game.screen, (30, 30, 30), is_game_scene=False)
game.add_scene(inv_scene)

game.change_scene(1)


def btn_action(b: sm_button.sm_button):
    b.text = "game has been generated"
    game.change_scene(0)
def btn_quit(b: sm_button.sm_button):
    b.text = "wait game save"
    running = False
    pygame.quit()
    sys.exit()
def btn_inv(b: sm_button.sm_button):
    b.text = "Inventory loaded"
    game.change_scene(2)


# Main menu scene
menu_scene.add_text(
    sm_text.sm_text(
        "Main Menu",
        310,
        10,
        pygame.font.SysFont("arial", 42),
        (255, 255, 255),
    )
)

menu_scene.add_button(
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
menu_scene.add_button(
    sm_button.sm_button(
        400,
        100,
        200,
        250,
        "Inventory",
        (100, 0, 0),
        pygame.font.SysFont("arial", 42),
        (0, 0, 0),
        btn_action,
    )
)
menu_scene.add_button(
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
test_scene.add_player(
    sm_player.sm_player(
        (256 * 64) // 2,
        (256 * 64) // 2,
        "textures/sprites/player.png",
    )
)

# inventory scene
menu_scene.add_text(
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
