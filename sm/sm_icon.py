import pygame


class sm_icon:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        image,
    ):
        self.x = x
        self.y = y
        self.image = image
        self.image = pygame.transform.scale(self.image, (width, height))
