import pygame


class sm_camera:
    def __init__(
        self,
        width,
        height,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        scroll_l=15,
    ):
        self.rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.scroll_length = scroll_l
        self.first_update = True
        self.scroll_up = False
        self.scroll_down = False
        self.scroll_left = False
        self.scroll_right = False
        self.scroll_up_counter = 0
        self.scroll_down_counter = 0
        self.scroll_left_counter = 0
        self.scroll_right_counter = 0
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

        target_s = self.apply(target.rect)  # s stands for screenspace
        c_target_s = self.apply_pos(
            (target.rect.centerx, target.rect.centery)
        )  # c stands for center

        if scroll_style == 0:
            x = target.rect.centerx - self.SCREEN_WIDTH // 2
            y = target.rect.centery - self.SCREEN_HEIGHT // 2

        elif scroll_style == 1:
            # scroll camera
            if self.scroll_up:
                if self.scroll_up_counter < self.scroll_length:
                    y -= (self.SCREEN_HEIGHT - 32) // self.scroll_length
                    self.scroll_up_counter += 1
                else:
                    self.scroll_up = False
                    self.scroll_up_counter = 0
            elif self.scroll_down:
                if self.scroll_down_counter < self.scroll_length:
                    y += (self.SCREEN_HEIGHT - 32) // self.scroll_length
                    self.scroll_down_counter += 1
                else:
                    self.scroll_down = False
                    self.scroll_down_counter = 0

            if self.scroll_left:
                if self.scroll_left_counter < self.scroll_length:
                    x -= (self.SCREEN_WIDTH - 32) // self.scroll_length
                    self.scroll_left_counter += 1
                else:
                    self.scroll_left = False
                    self.scroll_left_counter = 0
            elif self.scroll_right:
                if self.scroll_right_counter < self.scroll_length:
                    x += (self.SCREEN_WIDTH - 32) // self.scroll_length
                    self.scroll_right_counter += 1
                else:
                    self.scroll_right = False
                    self.scroll_right_counter = 0

            # disable player movement lock when scrolling is done
            if not (
                self.scroll_up
                or self.scroll_down
                or self.scroll_left
                or self.scroll_right
            ):
                self.lock_player = False

            # check if camera needs to be scrolled
            #
            # 5 pixels more than center to avoid accidental scrolling
            if not (self.scroll_up or self.scroll_down):
                if c_target_s[1] <= -5:
                    self.scroll_up = True
                    self.lock_player = True
                elif c_target_s[1] >= self.SCREEN_HEIGHT + 5:
                    self.scroll_down = True
                    self.lock_player = True

            if not (self.scroll_left or self.scroll_right):
                if c_target_s[0] <= -5:
                    self.scroll_left = True
                    self.lock_player = True
                elif c_target_s[0] >= self.SCREEN_WIDTH + 5:
                    self.scroll_right = True
                    self.lock_player = True

        if self.first_update:
            x = target.rect.centerx - self.SCREEN_WIDTH // 2
            y = target.rect.centery - self.SCREEN_HEIGHT // 2
            self.first_update = False
            self.scroll_up = False
            self.scroll_down = False
            self.scroll_left = False
            self.scroll_right = False
            self.lock_player = False

        x = max(0, min(x, self.width - self.SCREEN_WIDTH))
        y = max(0, min(y, self.height - self.SCREEN_HEIGHT))

        self.rect.topleft = (x, y)
