import pygame
import sm_scene


class sm_game:
    scenes: list[sm_scene.sm_scene] = []
    current_scene: sm_scene.sm_scene
    screen: pygame.Surface
    clock: pygame.time.Clock

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
        self.current_scene = self.scenes[index]

    def add_scene(self, scene):
        self.scenes.append(scene)

    def draw_current_scene(self):
        self.current_scene.draw_texts()
        self.current_scene.draw_buttons()

        if self.current_scene.is_game_scene:
            self.current_scene.draw_enemies()
            self.current_scene.draw_player()

    def update(self):
        if self.current_scene.is_game_scene:
            self.current_scene.player.update()
            self.current_scene.update()
