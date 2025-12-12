import sys

import pygame

# import setup of classes and window
import setup

while setup.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            setup.running = False

        # send mouse button down to check buttons of current scene
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1 = left mouse button
                setup.game.current_scene.check_buttons(event.pos)

    # Updates
    setup.game.update()

    # Drawing
    setup.game.screen.fill(setup.game.current_scene.bg_color)
    setup.game.draw_current_scene()

    pygame.display.flip()
    setup.game.clock.tick(setup.FPS)

pygame.quit()
sys.exit()
