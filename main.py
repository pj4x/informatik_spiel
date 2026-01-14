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

    # inventory
    if dungeon_crawler.game.current_scene == 2:
        # draw selected in inv
        if dungeon_crawler.btn_selects.storage_slct >= 0:
            pygame.draw.rect(dungeon_crawler.game.screen, (0,255,0), (dungeon_crawler.storage_btns[dungeon_crawler.btn_selects.storage_slct][0]-1,dungeon_crawler.storage_btns[dungeon_crawler.btn_selects.storage_slct][1]-1, 52, 52), width=1,)
        if dungeon_crawler.btn_selects.equip_slct >= 0:
            pygame.draw.rect(dungeon_crawler.game.screen, (0,255,0), (dungeon_crawler.equip_btns[dungeon_crawler.btn_selects.equip_slct][0]-1,dungeon_crawler.equip_btns[dungeon_crawler.btn_selects.equip_slct][1]-1, 52, 52), width=1,)
        if dungeon_crawler.btn_selects.armor_slct >= 0:
            pygame.draw.rect(dungeon_crawler.game.screen, (0,255,0), (dungeon_crawler.armor_btns[dungeon_crawler.btn_selects.armor_slct][0]-1,dungeon_crawler.storage_btns[dungeon_crawler.btn_selects.armor_slct][1]-1, 52, 52), width=1,)

        # switch items in inventory if two are selected
        # switch storage and armor slot
        if dungeon_crawler.btn_selects.storage_slct >= 0 and dungeon_crawler.btn_selects.armor_slct >= 0:
            if dungeon_crawler.inv[0][dungeon_crawler.btn_selects.storage_slct] >= 0:
               if dungeon_crawler.items[dungeon_crawler.inv[0][dungeon_crawler.btn_selects.storage_slct]].type == 1:
                   # change IDs
                   temp = dungeon_crawler.inv[0][dungeon_crawler.btn_selects.storage_slct]
                   dungeon_crawler.inv[0][dungeon_crawler.btn_selects.storage_slct] = dungeon_crawler.inv[1][dungeon_crawler.btn_selects.armor_slct]
                   dungeon_crawler.inv[1][dungeon_crawler.btn_selects.armor_slct] = temp
                   # change pictures
                   # unselect
                   dungeon_crawler.btn_selects.storage_slct = -1
                   dungeon_crawler.btn_selects.armor_slct = -1
               else:
                   # cant put non armor item in armor slot
                   # unselect
                   dungeon_crawler.btn_selects.storage_slct = -1
                   dungeon_crawler.btn_selects.armor_slct = -1
            else:
                # change IDs
                dungeon_crawler.inv[0][dungeon_crawler.btn_selects.storage_slct] = dungeon_crawler.inv[1][dungeon_crawler.btn_selects.armor_slct]
                dungeon_crawler.inv[1][dungeon_crawler.btn_selects.armor_slct] = -1
                # change pictures
                # unselect
                dungeon_crawler.btn_selects.storage_slct = -1
                dungeon_crawler.btn_selects.armor_slct = -1

        # switch storage and equip
        if dungeon_crawler.btn_selects.storage_slct >= 0 and dungeon_crawler.btn_selects.equip_slct >= 0:
            if dungeon_crawler.inv[0][dungeon_crawler.btn_selects.storage_slct] >= 0:
                if dungeon_crawler.items[dungeon_crawler.inv[0][dungeon_crawler.btn_selects.storage_slct]].type == 0:
                   # change IDs
                   temp = dungeon_crawler.inv[0][dungeon_crawler.btn_selects.storage_slct]
                   dungeon_crawler.inv[0][dungeon_crawler.btn_selects.storage_slct] = dungeon_crawler.inv[2][dungeon_crawler.btn_selects.equip_slct]
                   dungeon_crawler.inv[2][dungeon_crawler.btn_selects.equip_slct] = temp
                   # change pictures
                   # unselect
                   dungeon_crawler.btn_selects.storage_slct = -1
                   dungeon_crawler.btn_selects.equip_slct = -1
                else:
                   # cant put non equip item in equip slot
                   # unselect
                   dungeon_crawler.btn_selects.storage_slct = -1
                   dungeon_crawler.btn_selects.equip_slct = -1
            else:
                # change IDs
                dungeon_crawler.inv[0][dungeon_crawler.btn_selects.storage_slct] = dungeon_crawler.inv[2][dungeon_crawler.btn_selects.equip_slct]
                dungeon_crawler.inv[2][dungeon_crawler.btn_selects.equip_slct] = -1
                # change pictures
                # unselect
                dungeon_crawler.btn_selects.storage_slct = -1
                dungeon_crawler.btn_selects.equip_slct = -1


    pygame.display.flip()
    dungeon_crawler.game.dt = (
        dungeon_crawler.game.clock.tick(dungeon_crawler.FPS) / 1000
    )

pygame.quit()
sys.exit()
