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

test_scene = sm_scene.sm_scene(game.screen, (30, 30, 30), is_game_scene=True)
game.add_scene(test_scene)
game.change_scene(0)


txt = sm_text.sm_text("TEST", 0, 500, pygame.font.SysFont("arial", 32), (255, 255, 255))


def btn_action(b: sm_button.sm_button):
    b.text = "pressed"


btn = sm_button.sm_button(
    100,
    50,
    0,
    0,
    "test",
    (255, 0, 0),
    pygame.font.SysFont("arial", 16),
    (0, 0, 0),
    btn_action,
)

pp = sm_player.sm_player(400, 300, "textures/sprites/player.png")

test_scene.add_text(txt)
test_scene.add_button(btn)
test_scene.add_player(pp)


##################################################################
#
##################################################################
