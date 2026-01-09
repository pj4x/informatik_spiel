import pygame


class sm_button:
    def __init__(
        self,
        WIDTH,
        HEIGHT,
        x,
        y,
        text,
        color,
        font: pygame.font.Font,
        f_color,
        action=None,
    ):
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font
        self.f_color = f_color
        if action:
            self.action = action

    def action(self, pos):
        print("WARNING: Button has no action attached")
