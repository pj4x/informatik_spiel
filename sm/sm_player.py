import pygame


class sm_player(pygame.sprite.Sprite):
    def __init__(
        self,
        x,
        y,
        image_path,
    ):
        super().__init__()

        # Load the PNG texture with alpha transparency
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

        # Rect for positioning
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
