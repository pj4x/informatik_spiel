import sys

import pygame

# import setup of classes and window
import dungeon_crawler


while dungeon_crawler.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dungeon_crawler.running = False

        # send mouse button down to check buttons of current scene
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1 = left mouse button
                dungeon_crawler.game.scenes[
                    dungeon_crawler.game.current_scene
                ].check_buttons(event.pos)

    # Updates
    dungeon_crawler.game.update()

    # Drawing
    dungeon_crawler.game.screen.fill(
        dungeon_crawler.game.scenes[dungeon_crawler.game.current_scene].bg_color
    )
    dungeon_crawler.game.draw_current_scene()

    # draw selected in inv
    if dungeon_crawler.game.current_scene == 2:
        if dungeon_crawler.btn_selects.storage_slct >= 0:
            pygame.draw.rect(dungeon_crawler.game.screen, (0,255,0), (dungeon_crawler.storage_btns[dungeon_crawler.btn_selects.storage_slct][0]-1,dungeon_crawler.storage_btns[dungeon_crawler.btn_selects.storage_slct][1]-1, 52, 52), width=1,)
        if dungeon_crawler.btn_selects.equip_slct >= 0:
            pygame.draw.rect(dungeon_crawler.game.screen, (0,255,0), (dungeon_crawler.equip_btns[dungeon_crawler.btn_selects.equip_slct][0]-1,dungeon_crawler.equip_btns[dungeon_crawler.btn_selects.equip_slct][1]-1, 52, 52), width=1,)
        if dungeon_crawler.btn_selects.armor_slct >= 0:
            pygame.draw.rect(dungeon_crawler.game.screen, (0,255,0), (dungeon_crawler.armor_btns[dungeon_crawler.btn_selects.armor_slct][0]-1,dungeon_crawler.storage_btns[dungeon_crawler.btn_selects.armor_slct][1]-1, 52, 52), width=1,)
    
    
    pygame.display.flip()
    dungeon_crawler.game.dt = (
        dungeon_crawler.game.clock.tick(dungeon_crawler.FPS) / 1000
    )

pygame.quit()
sys.exit()
