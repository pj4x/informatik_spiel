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
        self.first_update = True
        self.scroll_up = False
        self.scroll_down = False
        self.scroll_left = False
        self.scroll_right = False
        self.lock_player = False

    def apply(self, target_rect):
        # apply offset to a rect (used for sprites)
        return (
            target_rect.x - self.rect.x,
            target_rect.y - self.rect.y,
        )

    def apply_pos(self, pos):
        # apply to manual x,y positions
        return (pos[0] - self.rect.x, pos[1] - self.rect.y)

    def update(self, target, scroll_style=0):
        # IMPORTANT: start from current position
        x, y = self.rect.topleft

        if self.first_update:
            x = target.rect.centerx - self.SCREEN_WIDTH // 2
            y = target.rect.centery - self.SCREEN_HEIGHT // 2
            self.first_update = False

        if scroll_style == 0:
            x = target.rect.centerx - self.SCREEN_WIDTH // 2
            y = target.rect.centery - self.SCREEN_HEIGHT // 2

        elif scroll_style == 1:
            inc_y = (self.SCREEN_HEIGHT + 37) // 15
            inc_x = (self.SCREEN_WIDTH + 37) // 15

            if self.scroll_up:
                if (target.rect.centery - self.rect.y) < (-5 + inc_y * 15):
                    y -= inc_y
                else:
                    self.scroll_up = False

            elif self.scroll_down:
                if (target.rect.centery - self.rect.y) > 37:
                    y += inc_y
                else:
                    self.scroll_down = False

            if self.scroll_left:
                if (target.rect.centerx - self.rect.x) < (-5 + inc_x * 15):
                    x -= inc_x
                else:
                    self.scroll_left = False

            elif self.scroll_right:
                if (target.rect.centerx - self.rect.x) > 37:
                    x += inc_x
                else:
                    self.scroll_right = False

            if not (
                self.scroll_up
                or self.scroll_down
                or self.scroll_left
                or self.scroll_right
            ):
                self.lock_player = False

            if not (self.scroll_up or self.scroll_down):
                if (target.rect.centery - self.rect.y) <= -5:
                    self.scroll_up = True
                    self.lock_player = True
                elif (target.rect.centery - self.rect.y) >= self.SCREEN_HEIGHT + 5:
                    self.scroll_down = True
                    self.lock_player = True

            if not (self.scroll_left or self.scroll_right):
                if (target.rect.centerx - self.rect.x) <= -5:
                    self.scroll_left = True
                    self.lock_player = True
                elif (target.rect.centerx - self.rect.x) >= self.SCREEN_WIDTH + 5:
                    self.scroll_right = True  # FIXED
                    self.lock_player = True

        x = max(0, min(x, self.width - self.SCREEN_WIDTH))
        y = max(0, min(y, self.height - self.SCREEN_HEIGHT))

        self.rect.topleft = (x, y)
