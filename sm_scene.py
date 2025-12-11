import pygame

import sm_button
import sm_enemy
import sm_text


class sm_scene:
    enemies: list[sm_enemy.sm_enemy] = []
    buttons: list[sm_button.sm_button] = []
    texts: list[sm_text.sm_text] = []
    screen: pygame.Surface
    is_game_scene = False
    bg_color = (0, 0, 0)

    def __init__(self, s, f, bg, update=None):
        pygame.font.init()
        self.screen = s
        self.font = f
        self.bg_color = bg
        if update:
            self.update = update

    def update(self):
        print("WARNING: scence has no update loop")

    def add_button(self, button: sm_button.sm_button):
        self.buttons.append(button)

    def add_text(self, text: sm_text.sm_text):
        self.texts.append(text)

    def draw_buttons(self):
        for i in self.buttons:
            pygame.draw.rect(self.screen, i.color, (i.x, i.y, i.WIDTH, i.HEIGHT))
            text_surface = self.font.render(i.text, True, (0, 0, 0))
            self.screen.blit(
                text_surface,
                (
                    i.x + i.WIDTH // 2 - text_surface.get_width() // 2,
                    i.y + i.HEIGHT // 2 - text_surface.get_height() // 2,
                ),
            )

    def draw_texts(self):
        for i in self.texts:
            text_surface = self.font.render(i.text, True, (255, 255, 255))
            self.screen.blit(text_surface, (i.x, i.y))

    def draw_enemies(self):
        print("TODO")
