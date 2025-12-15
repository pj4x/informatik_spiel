import sys

import pygame

# only for tests counter variabel
counter = 0
# import setup of classes and window
import setup

while setup.running == True:
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

    # du huso das kann nicht funktionieren wenn ich in einer nicht game scene bin du musst das mit einer abfrage machen ob es überhaupt einen player gibt 
    try:
        print(setup.game.current_scene.player.rect.topleft)
    except:
        counter += 1
        if counter > 100:
            print("no player in this scene")
            counter = 0

    pygame.display.flip()
    setup.game.clock.tick(setup.FPS)

pygame.quit()
sys.exit()
