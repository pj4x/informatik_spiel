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
        # draw player and enemies if current scene is game scene
        if self.current_scene.is_game_scene:
            self.current_scene.draw_enemies()
            self.current_scene.draw_player()

        # draw hud elements
        self.current_scene.draw_texts()
        self.current_scene.draw_buttons()

    def update(self):
        # run update functions for scene and player if current scene is game scene
        if self.current_scene.is_game_scene:
            self.current_scene.player.update()
            self.current_scene.update()
