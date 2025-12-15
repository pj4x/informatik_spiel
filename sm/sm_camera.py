import pygame


class sm_camera:
    def __init__(
        self,
        width,
        height,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
    ):
        self.rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN_WIDTH = SCREEN_WIDTH

    def apply(self, target_rect):
        # apply offset to a rect (used for sprites)
        return (
            target_rect.x - self.rect.x,
            target_rect.y - self.rect.y,
        )

    def apply_pos(self, pos):
        # apply to manual x,y positions
        return (pos[0] - self.rect.x, pos[1] - self.rect.y)

    def update(self, target):
        # center camera on target
        x = target.rect.centerx - self.SCREEN_WIDTH // 2
        y = target.rect.centery - self.SCREEN_HEIGHT // 2

        # limit scrolling
        x = max(0, min(x, self.width - self.SCREEN_WIDTH))
        y = max(0, min(y, self.height - self.SCREEN_HEIGHT))

        self.rect.topleft = (x, y)
