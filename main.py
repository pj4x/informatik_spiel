import sys

import pygame

import sm_button
import sm_enemy
import sm_game
import sm_scene
import sm_text

WIDTH, HEIGHT = 800, 600
FPS = 60
name = "t-t-t-test"
running = True

##################################################################
# Initialise classes
##################################################################
game = sm_game.sm_game(WIDTH, HEIGHT, name, FPS)

test_scene = sm_scene.sm_scene(game.screen, game.font, (30, 30, 30))
game.add_scene(test_scene)
game.change_scene(0)

txt = sm_text.sm_text("TEST", WIDTH // 2, HEIGHT // 2)
btn = sm_button.sm_button(200, 100, 0, 0, "test", (255, 0, 0))

test_scene.add_text(txt)
test_scene.add_button(btn)
##################################################################
#
##################################################################

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.draw_current_scene_hud()

    pygame.display.flip()
    game.clock.tick(FPS)

pygame.quit()
sys.exit()
