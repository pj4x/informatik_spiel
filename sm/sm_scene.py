from multiprocessing import set_forkserver_preload

import pygame
import sm_button
import sm_enemy
import sm_player
import sm_text


class sm_scene:
    enemies: list[sm_enemy.sm_enemy] = []
    buttons: list[sm_button.sm_button] = []
    texts: list[sm_text.sm_text] = []
    screen: pygame.Surface
    bg_color = (0, 0, 0)
    player: sm_player.sm_player

    def __init__(self, s, f, bg, update=None, is_game_scene=False):
        pygame.font.init()
        self.screen = s
        self.font = f
        self.bg_color = bg
        if update:
            self.update = update
        self.is_game_scene = is_game_scene

    def update(self):
        pass

    def add_button(self, button: sm_button.sm_button):
        self.buttons.append(button)

    def add_text(self, text: sm_text.sm_text):
        self.texts.append(text)

    def add_player(self, p: sm_player.sm_player):
        if self.is_game_scene:
            self.player = p
        else:
            print("WARNING: cant add player to none game scene")

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
        if self.is_game_scene:
            pass  # TODO

    def draw_player(self):
        if self.is_game_scene:
            self.screen.blit(self.player.image, self.player.rect)

    def check_buttons(self, pos):
        for i in self.buttons:
            if (
                i.x <= pos[0]
                and i.x + i.WIDTH >= pos[0]
                and i.y <= pos[1]
                and i.y + i.HEIGHT >= pos[1]
            ):
                i.action(i)
