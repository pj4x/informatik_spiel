import random
import sys

import pygame

# add sm subfolder to path
sys.path.insert(1, "./sm/")

import sm_button
import sm_enemy
import sm_game
import sm_icon
import sm_item
import sm_load
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


# Variables for inventory
class selec:
    storage_slct = -1
    equip_slct = -1
    armor_slct = -1

    def change_strg(self, x):
        self.storage_slct = x

    def change_equip(self, x):
        self.equip_slct = x

    def change_armor(self, x):
        self.armor_slct = x


btn_selects = selec()

storage_btns = []
armor_btns = []
equip_btns = []

inv = sm_load.load_inventory("data/data.db")


##################################################################
# Initialise classes and tilemap
##################################################################

# dont actually need to provide tile size since we use standard(64), but for consistency sake
game = sm_game.sm_game(
    WIDTH, HEIGHT, name, FPS, TILE_SIZE=TILE_SIZE, cam_scroll_style=1
)

empty_texture = pygame.image.load("textures/icons/empty.png").convert_alpha()

# load item data from db
items = sm_load.load_items_from_db("data/data.db")

# load textures for items
for i in items:
    i.image = pygame.image.load(i.image).convert_alpha()

# adding scenes to main scene array
game.add_scene(sm_scene.sm_scene(game.screen, (30, 30, 30), "test", is_game_scene=True))
game.add_scene(
    sm_scene.sm_scene(game.screen, (30, 30, 30), "menu", is_game_scene=False)
)
game.add_scene(sm_scene.sm_scene(game.screen, (30, 30, 30), "inv", is_game_scene=False))
game.change_scene(1)


def btn_game(b: sm_button.sm_button, pos):
    game.change_scene(0)


def btn_menu(b: sm_button.sm_button, pos):
    game.change_scene(1)


def btn_quit(b: sm_button.sm_button, pos):
    pygame.quit()
    sys.exit()


def btn_inv(b: sm_button.sm_button, pos):
    game.change_scene(2)


def btn_storage(b: sm_button.sm_button, pos):
    for i in range(len(storage_btns)):
        if (
            storage_btns[i][0] <= pos[0]
            and storage_btns[i][0] + 50 >= pos[0]
            and storage_btns[i][1] <= pos[1]
            and storage_btns[i][1] + 50 >= pos[1]
        ):
            # select or unselect
            if btn_selects.storage_slct == i:
                btn_selects.change_strg(-1)
            else:
                btn_selects.change_strg(i)
            break


def btn_armor(b: sm_button.sm_button, pos):
    for i in range(len(armor_btns)):
        if (
            armor_btns[i][0] <= pos[0]
            and armor_btns[i][0] + 50 >= pos[0]
            and armor_btns[i][1] <= pos[1]
            and armor_btns[i][1] + 50 >= pos[1]
        ):
            # select or unselect
            if btn_selects.armor_slct == i:
                btn_selects.change_armor(-1)
            else:
                btn_selects.change_armor(i)
            break


def btn_equip(b: sm_button.sm_button, pos):
    for i in range(len(equip_btns)):
        if (
            equip_btns[i][0] <= pos[0]
            and equip_btns[i][0] + 50 >= pos[0]
            and equip_btns[i][1] <= pos[1]
            and equip_btns[i][1] + 50 >= pos[1]
        ):
            # select or unselect
            if btn_selects.equip_slct == i:
                btn_selects.change_equip(-1)
            else:
                btn_selects.change_equip(i)
            break


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
        btn_game,
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


# Start with all walls
tilemap = [[1 for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]


def carve_block(x, y):
    """Carve a 2x2 path block"""
    for dy in (0, 1):
        for dx in (0, 1):
            if 0 <= x + dx < MAP_SIZE and 0 <= y + dy < MAP_SIZE:
                tilemap[y + dy][x + dx] = 0


def generate_maze():
    stack = []

    start_x = random.randrange(1, MAP_SIZE - 2, 4)
    start_y = random.randrange(1, MAP_SIZE - 2, 4)

    carve_block(start_x, start_y)
    stack.append((start_x, start_y))

    while stack:
        x, y = stack[-1]

        directions = [(4, 0), (-4, 0), (0, 4), (0, -4)]
        random.shuffle(directions)

        carved = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 1 <= nx < MAP_SIZE - 2 and 1 <= ny < MAP_SIZE - 2:
                if tilemap[ny][nx] == 1:
                    # carve corridor
                    carve_block(x + dx // 2, y + dy // 2)
                    carve_block(nx, ny)
                    stack.append((nx, ny))
                    carved = True
                    break

        if not carved:
            stack.pop()


generate_maze()
for y in range(127, 130):
    for x in range(127, 130):
        tilemap[y][x] = 0


tiles = [
    pygame.image.load("textures/map/brick_wall.png").convert_alpha(),  # 1
]

# Ensure correct size
tiles = [pygame.transform.scale(t, (TILE_SIZE, TILE_SIZE)) for t in tiles]

# tiles with collision
collides = [1]

game.scenes[0].add_map(tilemap, tiles, collides)


# inventory scene
game.scenes[2].add_text(
    sm_text.sm_text(
        "Inventory",
        300,
        5,
        pygame.font.SysFont("arial", 42),
        (255, 255, 255),
    )
)


game.scenes[2].add_text(
    sm_text.sm_text(
        "Storage",
        535,
        40,
        pygame.font.SysFont("arial", 24),
        (255, 255, 255),
    )
)

game.scenes[2].add_text(
    sm_text.sm_text(
        "Player Equipement",
        40,
        40,
        pygame.font.SysFont("arial", 24),
        (255, 255, 255),
    )
)


# inventory storage
for i in range(6):
    for j in range(7):
        game.scenes[2].add_button(
            sm_button.sm_button(
                50,
                50,
                380 + (i * 70),
                80 + (j * 70),
                "",
                (105, 105, 105),
                pygame.font.SysFont("arial", 42),
                (0, 0, 0),
                btn_storage,
            )
        )
        # set texture of icon to item in that slot
        index = (i * 7) + j
        img = empty_texture
        if inv[0][index] > -1 and inv[0][index] < len(items):
            img = items[inv[0][index]].image

        game.scenes[2].add_icon(
            sm_icon.sm_icon(
                380 + (i * 70),
                80 + (j * 70),
                50,
                50,
                img
            )
        )
        storage_btns.append((380 + (i * 70), 80 + (j * 70)))


# two armor slots
for i in range(2):
    game.scenes[2].add_button(
        sm_button.sm_button(
            50,
            50,
            250,
            80 + (i * 70),
            "",
            (105, 105, 105),
            pygame.font.SysFont("arial", 42),
            (0, 0, 0),
            btn_armor,
        )
    )
    # set texture
    img = empty_texture
    if inv[1][i] > -1 and inv[1][i] < len(items):
        img = items[inv[0][i]].image

    game.scenes[2].add_icon(
        sm_icon.sm_icon(
            250,
            80 + (i * 70),
            50,
            50,
            img
        )
    )
    armor_btns.append((250, 80 + (i * 70)))

# four equip slots
for i in range(4):
    game.scenes[2].add_button(
        sm_button.sm_button(
            50,
            50,
            40 + (i * 70),
            360,
            "",
            (105, 105, 105),
            pygame.font.SysFont("arial", 42),
            (0, 0, 0),
            btn_equip,
        )
    )
    # set textures
    # set texture
    img = empty_texture
    if inv[2][i] > -1 and inv[2][i] < len(items):
        img = items[inv[0][i]].image

    game.scenes[2].add_icon(
        sm_icon.sm_icon(
            40 + (i * 70),
            360,
            50,
            50,
            img
        )
    )
    equip_btns.append((40 + (i * 70), 360))

# player icon
# TODO change image
game.scenes[2].add_icon(
    sm_icon.sm_icon(
        40,
        80,
        190,
        260,
        pygame.image.load("textures/sprites/player.png").convert_alpha(),
    )
)

game.scenes[2].add_button(
    sm_button.sm_button(
        190,
        50,
        40,
        500,
        "Back to Main Menu",
        (0, 255, 0),
        pygame.font.SysFont("arial", 20),
        (0, 0, 0),
        btn_menu,
    )
)


##################################################################
#
##################################################################
