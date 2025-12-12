import pygame


class sm_enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        img,
        damage,
        hp,
        x,
        y,
        image_path,
    ):
        self.img = img
        self.damage = damage
        self.hp = hp
        self.x = x
        self.y = y

        # Load the PNG texture with alpha transparency
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

        # Rect for positioning
        self.rect = self.image.get_rect(topleft=(x, y))
