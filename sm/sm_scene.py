import pygame
import sm_button
import sm_camera
import sm_enemy
import sm_player
import sm_text


class sm_scene:
    screen: pygame.Surface
    bg_color = (0, 0, 0)
    player: sm_player.sm_player

    def __init__(
        self,
        s,
        bg,
        name,
        update=None,
        is_game_scene=False,
    ):
        pygame.font.init()
        self.screen = s
        self.bg_color = bg
        self.name = name
        if update:
            self.update = update
        self.is_game_scene = is_game_scene
        if is_game_scene:
            self.camera = sm_camera.sm_camera(256 * 64, 256 * 64, 800, 600)

    def update(self):
        pass

    ##################################################################
    # add functions
    ##################################################################
    def add_button(self, button: sm_button.sm_button):
        try:
            self.buttons.append(button)
        except:
            self.buttons: list[sm_button.sm_button] = []
            self.buttons.append(button)

    def add_text(self, text: sm_text.sm_text):
        try:
            self.texts.append(button)
        except:
            self.texts: list[sm_text.sm_text] = []
            self.texts.append(text)

    def add_player(self, p: sm_player.sm_player):
        if self.is_game_scene:
            self.player = p
        else:
            print("WARNING: cant add player to none game scene")
    
    def add_enemy(self, e: sm_enemy):
        try:
            self.enemies.append(e)
        except:
            enemies: list[sm_enemy.sm_enemy] = []
            self.enemies.append(e)

    ##################################################################
    # hud functions
    ##################################################################
    def check_buttons(self, pos):
        try:
            for i in self.buttons:
                if (
                    i.x <= pos[0]
                    and i.x + i.WIDTH >= pos[0]
                    and i.y <= pos[1]
                    and i.y + i.HEIGHT >= pos[1]
                ):
                    i.action(i)
        except:
            pass
