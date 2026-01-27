import pygame


def get_nearby_solid_tiles(player_rect, tilemap, TILE_SIZE, collide=None):
    tiles = []

    left = player_rect.left // TILE_SIZE
    right = player_rect.right // TILE_SIZE
    top = player_rect.top // TILE_SIZE
    bottom = player_rect.bottom // TILE_SIZE

    for y in range(top, bottom + 1):
        if y < 0 or y >= len(tilemap):
            continue

        for x in range(left, right + 1):
            if x < 0 or x >= len(tilemap[y]):
                continue

            tile_id = tilemap[y][x]
            if tile_id in collide:
                tiles.append(
                    pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

    return tiles
