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
game.add_scene(sm_scene.sm_scene(game.screen, (30, 30, 30), "test", is_game_scene=True))
game.add_scene(sm_scene.sm_scene(game.screen, (30, 30, 30), "menu", is_game_scene=False))
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
        "textures/sprites/player.png",
    )
)

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
