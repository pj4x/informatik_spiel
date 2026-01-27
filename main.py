import math
import os
import random
import sys

import pygame

# import setup of classes and window
import dungeon_crawler

sys.path.insert(1, "./sm/")
import sm_load

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

    if dungeon_crawler.game.current_scene == 0:
        # player extraction
        if dungeon_crawler.game.scenes[0].player.extract:
            sm_load.store_inventory(
                "data/data.db",
                dungeon_crawler.inv.inv[0],
                dungeon_crawler.inv.inv[1],
                dungeon_crawler.inv.inv[2],
            )
            os.execv(sys.executable, [sys.executable] + sys.argv)

        # player open chest
        if dungeon_crawler.game.scenes[0].player.give_item:
            for i in range(42):
                if dungeon_crawler.inv.inv[0][i] == -1:
                    item = random.choice(dungeon_crawler.items)
                    dungeon_crawler.inv.inv[0][i] = item.ID
                    break
        dungeon_crawler.game.scenes[0].player.give_item = False

        # player attack
        if dungeon_crawler.game.scenes[0].player.attack:
            for enemy in dungeon_crawler.game.scenes[0].enemies:
                distance = math.hypot(
                    dungeon_crawler.game.scenes[0].player.rect.topleft[0] - enemy.x,
                    dungeon_crawler.game.scenes[0].player.rect.topleft[1] - enemy.y,
                )
                if distance <= 55:
                    enemy.hp -= 5
            dungeon_crawler.game.scenes[0].player.attack = False

    # inventory
    if dungeon_crawler.game.current_scene == 2:
        # draw selected in inv
        if dungeon_crawler.btn_selects.storage_slct >= 0:
            pygame.draw.rect(
                dungeon_crawler.game.screen,
                (0, 255, 0),
                (
                    dungeon_crawler.storage_btns[
                        dungeon_crawler.btn_selects.storage_slct
                    ][0]
                    - 2,
                    dungeon_crawler.storage_btns[
                        dungeon_crawler.btn_selects.storage_slct
                    ][1]
                    - 2,
                    54,
                    54,
                ),
                width=1,
            )
        if dungeon_crawler.btn_selects.equip_slct >= 0:
            pygame.draw.rect(
                dungeon_crawler.game.screen,
                (0, 255, 0),
                (
                    dungeon_crawler.equip_btns[dungeon_crawler.btn_selects.equip_slct][
                        0
                    ]
                    - 2,
                    dungeon_crawler.equip_btns[dungeon_crawler.btn_selects.equip_slct][
                        1
                    ]
                    - 2,
                    54,
                    54,
                ),
                width=1,
            )
        if dungeon_crawler.btn_selects.armor_slct >= 0:
            pygame.draw.rect(
                dungeon_crawler.game.screen,
                (0, 255, 0),
                (
                    dungeon_crawler.armor_btns[dungeon_crawler.btn_selects.armor_slct][
                        0
                    ]
                    - 2,
                    dungeon_crawler.storage_btns[
                        dungeon_crawler.btn_selects.armor_slct
                    ][1]
                    - 2,
                    54,
                    54,
                ),
                width=1,
            )

        # deselect if armor and equip slots are selected
        if (
            dungeon_crawler.btn_selects.armor_slct >= 0
            and dungeon_crawler.btn_selects.equip_slct >= 0
        ):
            dungeon_crawler.btn_selects.change_equip(-1)
            dungeon_crawler.btn_selects.change_armor(-1)
        # switch items in inventory if two are selected
        # switch storage and armor slot
        if (
            dungeon_crawler.btn_selects.storage_slct >= 0
            and dungeon_crawler.btn_selects.armor_slct >= 0
        ):
            if (
                dungeon_crawler.inv.inv[0][dungeon_crawler.btn_selects.storage_slct]
                >= 0
            ):
                if (
                    dungeon_crawler.items[
                        dungeon_crawler.inv.inv[0][
                            dungeon_crawler.btn_selects.storage_slct
                        ]
                    ].type
                    == 1
                ):
                    # change IDs
                    temp = dungeon_crawler.inv.inv[0][
                        dungeon_crawler.btn_selects.storage_slct
                    ]
                    dungeon_crawler.inv.inv[0][
                        dungeon_crawler.btn_selects.storage_slct
                    ] = dungeon_crawler.inv.inv[1][
                        dungeon_crawler.btn_selects.armor_slct
                    ]
                    dungeon_crawler.inv.inv[1][
                        dungeon_crawler.btn_selects.armor_slct
                    ] = temp
                    # change pictures
                    temp = (
                        dungeon_crawler.game.scenes[2]
                        .icons[dungeon_crawler.btn_selects.storage_slct]
                        .image
                    )
                    dungeon_crawler.game.scenes[2].icons[
                        dungeon_crawler.btn_selects.storage_slct
                    ].image = (
                        dungeon_crawler.game.scenes[2]
                        .icons[42 + dungeon_crawler.btn_selects.armor_slct]
                        .image
                    )
                    dungeon_crawler.game.scenes[2].icons[
                        42 + dungeon_crawler.btn_selects.armor_slct
                    ].image = temp
                    # unselect
                    dungeon_crawler.btn_selects.change_strg(-1)
                    dungeon_crawler.btn_selects.change_armor(-1)
                else:
                    # cant put non armor item in armor slot
                    # unselect
                    dungeon_crawler.btn_selects.change_strg(-1)
                    dungeon_crawler.btn_selects.change_armor(-1)
            else:
                # change IDs
                dungeon_crawler.inv.inv[0][dungeon_crawler.btn_selects.storage_slct] = (
                    dungeon_crawler.inv.inv[1][dungeon_crawler.btn_selects.armor_slct]
                )
                dungeon_crawler.inv.inv[1][dungeon_crawler.btn_selects.armor_slct] = -1
                # change pictures
                temp = (
                    dungeon_crawler.game.scenes[2]
                    .icons[dungeon_crawler.btn_selects.storage_slct]
                    .image
                )
                dungeon_crawler.game.scenes[2].icons[
                    dungeon_crawler.btn_selects.storage_slct
                ].image = (
                    dungeon_crawler.game.scenes[2]
                    .icons[42 + dungeon_crawler.btn_selects.armor_slct]
                    .image
                )
                dungeon_crawler.game.scenes[2].icons[
                    42 + dungeon_crawler.btn_selects.armor_slct
                ].image = temp
                # unselect
                dungeon_crawler.btn_selects.change_strg(-1)
                dungeon_crawler.btn_selects.change_armor(-1)

        # switch storage and equip
        if (
            dungeon_crawler.btn_selects.storage_slct >= 0
            and dungeon_crawler.btn_selects.equip_slct >= 0
        ):
            if (
                dungeon_crawler.inv.inv[0][dungeon_crawler.btn_selects.storage_slct]
                >= 0
            ):
                if (
                    dungeon_crawler.items[
                        dungeon_crawler.inv.inv[0][
                            dungeon_crawler.btn_selects.storage_slct
                        ]
                    ].type
                    == 0
                ):
                    # change IDs
                    temp = dungeon_crawler.inv.inv[0][
                        dungeon_crawler.btn_selects.storage_slct
                    ]
                    dungeon_crawler.inv.inv[0][
                        dungeon_crawler.btn_selects.storage_slct
                    ] = dungeon_crawler.inv.inv[2][
                        dungeon_crawler.btn_selects.equip_slct
                    ]
                    dungeon_crawler.inv.inv[2][
                        dungeon_crawler.btn_selects.equip_slct
                    ] = temp
                    # change pictures
                    temp = (
                        dungeon_crawler.game.scenes[2]
                        .icons[dungeon_crawler.btn_selects.storage_slct]
                        .image
                    )
                    dungeon_crawler.game.scenes[2].icons[
                        dungeon_crawler.btn_selects.storage_slct
                    ].image = (
                        dungeon_crawler.game.scenes[2]
                        .icons[44 + dungeon_crawler.btn_selects.equip_slct]
                        .image
                    )
                    dungeon_crawler.game.scenes[2].icons[
                        44 + dungeon_crawler.btn_selects.equip_slct
                    ].image = temp
                    # unselect
                    dungeon_crawler.btn_selects.change_strg(-1)
                    dungeon_crawler.btn_selects.change_equip(-1)
                else:
                    # cant put non equip item in equip slot
                    # unselect
                    dungeon_crawler.btn_selects.change_strg(-1)
                    dungeon_crawler.btn_selects.change_equip(-1)
            else:
                # change IDs
                dungeon_crawler.inv.inv[0][dungeon_crawler.btn_selects.storage_slct] = (
                    dungeon_crawler.inv.inv[2][dungeon_crawler.btn_selects.equip_slct]
                )
                dungeon_crawler.inv.inv[2][dungeon_crawler.btn_selects.equip_slct] = -1
                # change pictures
                temp = (
                    dungeon_crawler.game.scenes[2]
                    .icons[dungeon_crawler.btn_selects.storage_slct]
                    .image
                )
                dungeon_crawler.game.scenes[2].icons[
                    dungeon_crawler.btn_selects.storage_slct
                ].image = (
                    dungeon_crawler.game.scenes[2]
                    .icons[44 + dungeon_crawler.btn_selects.equip_slct]
                    .image
                )
                dungeon_crawler.game.scenes[2].icons[
                    44 + dungeon_crawler.btn_selects.equip_slct
                ].image = temp
                # unselect
                dungeon_crawler.btn_selects.change_strg(-1)
                dungeon_crawler.btn_selects.change_equip(-1)

    pygame.display.flip()
    dungeon_crawler.game.dt = (
        dungeon_crawler.game.clock.tick(dungeon_crawler.FPS) / 1000
    )

pygame.quit()
sys.exit()
