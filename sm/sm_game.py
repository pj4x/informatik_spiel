import math

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
        self.width, self.height = WIDTH, HEIGHT
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()
        self.cam_scroll_style = cam_scroll_style
        if TILE_SIZE:
            self.TILE_SIZE = TILE_SIZE

        self.sound_hit = pygame.mixer.Sound("sound_effects/hitHurt.wav")
        self.sound_explode = pygame.mixer.Sound("sound_effects/explosion.wav")

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
                    if enemy.hp <= 0:
                        continue
                    # Apply camera offset to enemy position
                    enemy_screen_pos = self.scenes[self.current_scene].camera.apply_pos(
                        (enemy.x, enemy.y)
                    )
                    # Draw enemy at screen position
                    self.screen.blit(enemy.image, enemy_screen_pos)
                    # draw enemy health bar
                    self.draw_enemy_health_bar(enemy, enemy_screen_pos)

            # draw player if alive
            if self.scenes[self.current_scene].player_alive:
                self.screen.blit(
                    self.scenes[self.current_scene].player.image,
                    self.scenes[self.current_scene].camera.apply(
                        self.scenes[self.current_scene].player.rect
                    ),
                )
            # draw player health bar
            self.draw_player_health_bar(
                self.scenes[self.current_scene].player.hp,
                self.scenes[self.current_scene].player.max_hp,
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

    def draw_enemy_health_bar(self, enemy, screen_pos):
        if enemy.hp <= 0:
            return

        # Health bar dimensions
        bar_width = 40
        bar_height = 4
        border_thickness = 1

        # Calculate health percentage
        health_percentage = enemy.hp / enemy.max_hp

        # Health bar position (above the enemy)
        bar_x = screen_pos[0] + 12  # center above enemy
        bar_y = screen_pos[1] - bar_height - 2  # 2 pixels above enemy

        # Draw border
        border_rect = pygame.Rect(
            bar_x - border_thickness,
            bar_y - border_thickness,
            bar_width + 2 * border_thickness,
            bar_height + 2 * border_thickness,
        )
        pygame.draw.rect(self.screen, (0, 0, 0), border_rect)

        # Draw background (empty health)
        background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (255, 0, 0), background_rect)

        # Draw current health
        health_width = int(bar_width * health_percentage)
        if health_width > 0:
            health_rect = pygame.Rect(bar_x, bar_y, health_width, bar_height)
            pygame.draw.rect(self.screen, (0, 255, 0), health_rect)

    def draw_player_health_bar(self, hp, max_hp):
        # Health bar dimensions
        bar_width = 200
        bar_height = 50
        border_thickness = 3

        # Calculate health percentage
        health_percentage = hp / max_hp

        # Health bar position (above the enemy)
        bar_x = 30
        bar_y = self.height - 70

        # Draw border
        border_rect = pygame.Rect(
            bar_x - border_thickness,
            bar_y - border_thickness,
            bar_width + 2 * border_thickness,
            bar_height + 2 * border_thickness,
        )
        pygame.draw.rect(self.screen, (0, 0, 0), border_rect)

        # Draw background (empty health)
        background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (255, 0, 0), background_rect)

        # Draw current health
        health_width = int(bar_width * health_percentage)
        if health_width > 0:
            health_rect = pygame.Rect(bar_x, bar_y, health_width, bar_height)
            pygame.draw.rect(self.screen, (0, 255, 0), health_rect)

    def update(self):
        # run update functions for scene and player if current scene is game scene
        if self.scenes[self.current_scene].is_game_scene:
            # Update enemies if scene has enemies
            if hasattr(self.scenes[self.current_scene], "enemies"):
                for enemy in self.scenes[self.current_scene].enemies:
                    if enemy.hp <= 0:
                        continue
                    # Update enemy animation and ai
                    #
                    # give real player position if alive, otherwise very large number
                    if self.scenes[self.current_scene].player_alive:
                        enemy.ai(self.scenes[self.current_scene].player.rect.topleft)
                    else:
                        enemy.ai((10**20, 10**20))
                    enemy.update(self.dt)
                    if enemy.hit and self.scenes[self.current_scene].player_alive:
                        distance = math.hypot(
                            self.scenes[self.current_scene].player.rect.topleft[0]
                            - enemy.x,
                            self.scenes[self.current_scene].player.rect.topleft[1]
                            - enemy.y,
                        )
                        if distance <= 64:
                            self.scenes[self.current_scene].player.hp -= enemy.damage
                            self.sound_hit.play()

            if self.scenes[self.current_scene].player_alive:
                if self.scenes[self.current_scene].player.hp <= 0:
                    self.sound_explode.play()
                    self.scenes[self.current_scene].player_alive = False

                # only update player when camera isnt moving with scrolling style 1
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
