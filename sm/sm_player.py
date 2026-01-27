import pygame
import sm_tilemap


class sm_player(pygame.sprite.Sprite):
    def __init__(
        self,
        x,
        y,
        speed,
        hp,
        image_path,
    ):
        super().__init__()

        # Load the PNG texture with alpha transparency
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.sound_pickup = pygame.mixer.Sound("sound_effects/pickupCoin.wav")

        # Rect for positioning
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = speed

        self.hp = hp
        self.max_hp = self.hp
        self.extract = False
        self.give_item = False
        self.attack = False
        self.attack_cooldown = 0

    def update(self, tilemap, cld):
        dx = dy = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed

        # ---- X movement ----
        self.rect.x += dx
        for tile in sm_tilemap.get_nearby_solid_tiles(
            self.rect, tilemap, 64, collide=cld
        ):
            if self.rect.colliderect(tile):
                if dx > 0:
                    self.rect.right = tile.left
                elif dx < 0:
                    self.rect.left = tile.right

        # ---- Y movement ----
        self.rect.y += dy
        for tile in sm_tilemap.get_nearby_solid_tiles(
            self.rect, tilemap, 64, collide=cld
        ):
            if self.rect.colliderect(tile):
                if dy > 0:
                    self.rect.bottom = tile.top
                elif dy < 0:
                    self.rect.top = tile.bottom

        if keys[pygame.K_e]:
            # chests
            for tile in sm_tilemap.get_nearby_solid_tiles(
                self.rect, tilemap, 64, collide=cld
            ):
                if tilemap[tile.y // 64][tile.x // 64] == 2:
                    self.sound_pickup.play()
                    tilemap[tile.y // 64][tile.x // 64] = 0
                    self.give_item = True

            # extraction point
            for tile in sm_tilemap.get_nearby_solid_tiles(
                self.rect, tilemap, 64, collide=cld
            ):
                if tilemap[tile.y // 64][tile.x // 64] == 3:
                    self.extract = True

        if keys[pygame.K_q]:
            # attack
            if self.attack_cooldown >= 15:
                self.attack = True
                self.attack_cooldown = 0
            else:
                self.attack_cooldown += 1
