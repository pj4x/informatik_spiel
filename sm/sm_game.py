from enum import EnumDict

import pygame
import sm_scene


class sm_game:
    scenes: list[sm_scene.sm_scene] = []
    screen: pygame.Surface
    clock: pygame.time.Clock
    current_scene = 0
    dt = 0.0

    def __init__(
        self,
        WIDTH,
        HEIGHT,
        name,
        FPS,
        TILE_SIZE=64,
        cam_scroll_style=0,
    ):
        # initialise pygame
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()
        self.cam_scroll_style = cam_scroll_style
        if TILE_SIZE:
            self.TILE_SIZE = TILE_SIZE

    def change_scene(self, index):
        self.current_scene = index

    def add_scene(self, scene):
        self.scenes.append(scene)

    def draw_current_scene(self):
        # draw player, enemies and tilemap if current scene is game scene
        if self.scenes[self.current_scene].is_game_scene:
            # draw tilemap
            start_col = (
                self.scenes[self.current_scene].camera.rect.left // self.TILE_SIZE
            )
            end_col = (
                self.scenes[self.current_scene].camera.rect.right // self.TILE_SIZE + 1
            )

            start_row = (
                self.scenes[self.current_scene].camera.rect.top // self.TILE_SIZE
            )
            end_row = (
                self.scenes[self.current_scene].camera.rect.bottom // self.TILE_SIZE + 1
            )

            for row in range(start_row, end_row):
                if row < 0 or row >= len(self.scenes[self.current_scene].tilemap):
                    continue

                for col in range(start_col, end_col):
                    if col < 0 or col >= len(
                        self.scenes[self.current_scene].tilemap[row]
                    ):
                        continue

                    tile_id = (
                        self.scenes[self.current_scene].tilemap[row][col] - 1
                    )  # subtract 1 so that tile_id 0 is empty tile
                    if tile_id < 0:
                        continue

                    world_x = col * self.TILE_SIZE
                    world_y = row * self.TILE_SIZE

                    screen_x, screen_y = self.scenes[
                        self.current_scene
                    ].camera.apply_pos((world_x, world_y))
                    self.screen.blit(
                        self.scenes[self.current_scene].tileset[tile_id],
                        (screen_x, screen_y),
                    )

            # draw enemies
            if hasattr(self.scenes[self.current_scene], "enemies"):
                for enemy in self.scenes[self.current_scene].enemies:
                    # Apply camera offset to enemy position
                    enemy_screen_pos = self.scenes[self.current_scene].camera.apply_pos(
                        (enemy.x, enemy.y)
                    )
                    # Draw enemy at screen position
                    self.screen.blit(enemy.image, enemy_screen_pos)

            # draw player
            self.screen.blit(
                self.scenes[self.current_scene].player.image,
                self.scenes[self.current_scene].camera.apply(
                    self.scenes[self.current_scene].player.rect
                ),
            )

        # draw texts
        try:
            for i in self.scenes[self.current_scene].texts:
                text_surface = i.font.render(i.text, True, i.f_color)
                self.screen.blit(text_surface, (i.x, i.y))
        except:
            pass

        # draw buttons
        try:
            for i in self.scenes[self.current_scene].buttons:
                pygame.draw.rect(self.screen, i.color, (i.x, i.y, i.WIDTH, i.HEIGHT))
                text_surface = i.font.render(i.text, True, i.f_color)
                self.screen.blit(
                    text_surface,
                    (
                        i.x + i.WIDTH // 2 - text_surface.get_width() // 2,
                        i.y + i.HEIGHT // 2 - text_surface.get_height() // 2,
                    ),
                )
        except:
            pass

        # draw icons
        try:
            for i in self.scenes[self.current_scene].icons:
                self.screen.blit(i.image, (i.x, i.y))
        except:
            pass

    def update(self):
        # run update functions for scene and player if current scene is game scene
        if self.scenes[self.current_scene].is_game_scene:
            # Update enemies if scene has enemies
            if hasattr(self.scenes[self.current_scene], "enemies"):
                for enemy in self.scenes[self.current_scene].enemies:
                    # Update enemy animation and ai
                    enemy.ai(self.scenes[self.current_scene].player.rect.topleft)
                    enemy.update(self.dt)
            # only update player when camera isnt moving
            if not self.scenes[self.current_scene].camera.lock_player:
                self.scenes[self.current_scene].player.update(
                    self.scenes[self.current_scene].tilemap,
                    self.scenes[self.current_scene].collides,
                )
            # update scene
            self.scenes[self.current_scene].update()

            # update camera
            self.scenes[self.current_scene].camera.update(
                self.scenes[self.current_scene].player,
                self.cam_scroll_style,
            )
