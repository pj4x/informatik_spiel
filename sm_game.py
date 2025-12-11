import pygame

import sm_scene


class sm_game:
    scenes: list[sm_scene.sm_scene] = []
    current_scene: sm_scene.sm_scene
    screen: pygame.Surface
    clock: pygame.time.Clock

    def __init__(self, WIDTH, HEIGHT, name, FPS):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 16)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()

    def change_scene(self, index):
        self.current_scene = self.scenes[index]

    def add_scene(self, scene):
        self.scenes.append(scene)

    def draw_current_scene_hud(self):
        self.screen.fill(self.current_scene.bg_color)
        self.current_scene.draw_texts()
        self.current_scene.draw_buttons()
