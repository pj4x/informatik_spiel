import pygame


class sm_text:
    def __init__(
        self,
        text,
        x,
        y,
        font: pygame.font.Font,
        f_color,
    ):
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.f_color = f_color
