import pygame
import sm_scene


class sm_game:
    scenes: list[sm_scene.sm_scene] = []
    screen: pygame.Surface
    clock: pygame.time.Clock
    current_scene = 0

    def __init__(
        self,
        WIDTH,
        HEIGHT,
        name,
        FPS,
    ):
        # initialise pygame
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()

    def change_scene(self, index):
        self.current_scene = index

    def add_scene(self, scene):
        self.scenes.append(scene)

    def draw_current_scene(self):
        # draw player and enemies if current scene is game scene
        if self.scenes[self.current_scene].is_game_scene:
            # draw enemies
            # TODO

            # draw player
            self.screen.blit(
                self.scenes[self.current_scene].player.image,
                self.scenes[self.current_scene].camera.apply(
                    self.scenes[self.current_scene].player.rect
                ),
            )

        # draw texts
        for i in self.scenes[self.current_scene].texts:
            text_surface = i.font.render(i.text, True, i.f_color)
            self.screen.blit(text_surface, (i.x, i.y))

        # draw buttons
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

    def update(self):
        # run update functions for scene and player if current scene is game scene
        if self.scenes[self.current_scene].is_game_scene:
            self.scenes[self.current_scene].player.update()
            self.scenes[self.current_scene].update()
            self.scenes[self.current_scene].camera.update(
                self.scenes[self.current_scene].player
            )
