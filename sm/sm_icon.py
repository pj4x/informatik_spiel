import pygame


class sm_icon:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        image_path,
    ):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
