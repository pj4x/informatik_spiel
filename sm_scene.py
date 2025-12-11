import pygame
import sm_button
import sm_entity
import sm_text

class sm_scene:
    entities: list[sm_entity.sm_entity] = []
    buttons: list[sm_button.sm_button] = []
    texts: list[sm_text.sm_text] = []
    screen = None
    font = pygame.font.Font(None, 16)

    def __init__(self, s):
        self.screen = s
        #TODO load textures

    def draw_buttons(self):
        for i in self.buttons:
            pygame.draw.rect(self.screen, i.color, (i.x, i.y, i.WIDTH, i.HEIGHT))
            text_surface = self.font.render(i.text, True, (0,0,0))
            self.screen.blit(text_surface, (i.x, i.y))

    def draw_texts(self):
        for i in self.texts:
            text_surface = self.font.render(i.text, True, (0,0,0))
            self.screen.blit(text_surface, (i.x, i.y))
    