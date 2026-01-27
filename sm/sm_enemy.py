import math
import random

import pygame


class sm_enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        damage,
        hp,
        x,
        y,
        img_root_path,
    ):
        super().__init__()

        self.damage = damage
        self.hp = hp
        self.max_hp = hp
        self.x = x
        self.y = y

        # Animation states
        self.current_action = "idle"  # idle, walk, attack
        self.current_direction = "down"  # up, down, left, right
        self.animation_frame = 0  # Current frame index (0-3)
        self.animation_speed = 0.15  # Time between frames
        self.frame_timer = 0
        self.attacking = False

        # Store loaded sprite sheets (each with 4 frames)
        self.sprites = {}

        # Load all sprite sheets
        self.load_sprite_sheets(img_root_path)

        # Set initial image and rect
        self.image = self.get_current_frame()
        self.rect = self.image.get_rect(topleft=(x, y))

        # variables for ai
        self.state = 0  # 0 = idle, 1 = go to player, 2 = attack, 3 = attacking
        self.ai_update_counter = 0

    def load_sprite_sheets(self, path):
        # Load all sprite sheets
        # Default structure for sprite sheet paths
        paths = {
            "idle": {
                "up": f"{path}idle_above.png",
                "down": f"{path}idle_down.png",
                "left": f"{path}idle_left.png",
                "right": f"{path}idle_right.png",
            },
            "walk": {
                "up": f"{path}walk_above.png",
                "down": f"{path}walk_down.png",
                "left": f"{path}walk_left.png",
                "right": f"{path}walk_right.png",
            },
            "attack": {
                "up": f"{path}attack_above.png",
                "down": f"{path}attack_down.png",
                "left": f"{path}attack_left.png",
                "right": f"{path}attack_right.png",
            },
        }

        for action in ["idle", "walk", "attack"]:
            if action in paths:
                self.sprites[action] = {}
                for direction in ["up", "down", "left", "right"]:
                    if direction in paths[action]:
                        path = paths[action][direction]
                        try:
                            sprite_sheet = pygame.image.load(path).convert_alpha()
                            self.sprites[action][direction] = self.parse_sprite_sheet(
                                sprite_sheet, 4
                            )
                        except (pygame.error, FileNotFoundError):
                            # Fallback to colored rectangles if image not found
                            print(
                                f"Warning: Could not load {action}_{direction} sprite sheet"
                            )
                            self.sprites[action][direction] = (
                                self.create_fallback_frames(4)
                            )

    def parse_sprite_sheet(self, sprite_sheet, num_frames=4, frame_width=32):
        # Parse a sprite sheet into exactly num_frames
        sheet_width, sheet_height = sprite_sheet.get_size()
        frames = []

        # Each animation has exactly 4 frames
        frame_width = sheet_width // num_frames

        for i in range(num_frames):
            frame_rect = pygame.Rect(i * frame_width, 0, frame_width, sheet_height)
            frame = sprite_sheet.subsurface(frame_rect)
            frame = pygame.transform.scale(frame, (64, 64))
            frames.append(frame)

        return frames

    def create_fallback_frames(self, num_frames):
        # Create simple colored rectangles as fallback frames
        frames = []
        colors = [(255, 0, 0), (200, 0, 0), (150, 0, 0), (100, 0, 0)]  # Red gradient

        for i in range(num_frames):
            surface = pygame.Surface((32, 32), pygame.SRCALPHA)
            color_idx = i % len(colors)
            pygame.draw.rect(surface, colors[color_idx], (0, 0, 32, 32))
            frames.append(surface)

        return frames

    def get_current_frame(self):
        # Get the current frame based on state and direction
        try:
            frames = self.sprites[self.current_action][self.current_direction]
            # Ensure we have exactly 4 frames, use modulo to stay within bounds
            frame_index = int(self.animation_frame) % 4
            return frames[frame_index]
        except (KeyError, IndexError):
            # Fallback if frames not found
            fallback_frames = self.create_fallback_frames(4)
            return fallback_frames[int(self.animation_frame) % 4]

    def set_action(self, action, direction=None):
        # Change the current action and optionally direction
        if action in ["idle", "walk", "attack"]:
            self.current_action = action

            if action == "attack":
                self.attacking = True
                self.animation_frame = 0  # Start attack animation from beginning

        if direction and direction in ["up", "down", "left", "right"]:
            self.current_direction = direction

    def update(self, dt):
        # Update animation frame
        self.frame_timer += dt

        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0
            self.animation_frame += 1

            # Keep animation_frame within 0-3 range for 4 frames
            if self.animation_frame >= 4:
                self.animation_frame = 0

                # Check if attack animation completed one cycle
                if self.current_action == "attack":
                    self.attacking = False
                    self.set_action("idle")  # Return to idle after attack

        # Update the current image
        self.image = self.get_current_frame()

    def move(self, dx, dy):
        # Move the enemy and set appropriate animation
        if dx != 0 or dy != 0:
            self.set_action("walk")

            # Set direction based on movement
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.current_direction = "right"
                else:
                    self.current_direction = "left"
            else:
                if dy > 0:
                    self.current_direction = "down"
                else:
                    self.current_direction = "up"

            self.x += dx
            self.y += dy
            self.rect.topleft = (self.x, self.y)
        else:
            # Not moving, go to idle
            if not self.attacking:
                self.set_action("idle")

    def attack(self, direction=None):
        # Start attack animation in specified direction or current direction
        if direction and direction in ["up", "down", "left", "right"]:
            self.current_direction = direction

        if not self.attacking:
            self.set_action("attack")

    def get_total_frames(self, action, direction):
        # Helper method to get total frames for an animation
        try:
            frames = self.sprites[action][direction]
            return len(frames)
        except (KeyError, IndexError):
            return 4  # Default to 4 frames

    def is_animation_complete(self):
        # Check if current animation has completed a full cycle
        return self.animation_frame == 0 and self.frame_timer == 0

    def ai(self, player_pos):
        # Update AI counter to limit how often AI logic runs
        self.ai_update_counter += 1
        if self.ai_update_counter < 10:  # update AI every 10 frames
            return
        self.ai_update_counter = 0

        # Compute distance to player
        px, py = player_pos
        dx = px - self.x
        dy = py - self.y
        distance = math.hypot(dx, dy)

        # Define detection and attack ranges
        detection_range = 300
        attack_range = 50
        if not self.attacking:
            if self.state == 0:  # idle
                # Random walk
                if random.randint(0, 100) < 20:  # small chance to move
                    self.move(
                        random.choice([-20, -10, 0, 10, 20]),
                        random.choice([-20, -10, 0, 10, 20]),
                    )
                else:
                    self.set_action("idle")

                # Transition to chase if player is close
                if distance <= detection_range:
                    self.state = 1

            elif self.state == 1:  # go to player
                # Move towards player
                speed = 10
                if distance != 0:
                    move_x = speed * dx / distance
                    move_y = speed * dy / distance
                    self.move(move_x, move_y)
                else:
                    self.move(0, 0)

                # Switch to attack if close enough
                if distance <= attack_range:
                    self.state = 2
                # Go back to idle if player moves far away
                elif distance > detection_range:
                    self.set_action("idle")
                    self.state = 0

            elif self.state == 2:  # attack
                self.attack()
                # Go back to chase if player moves out of attack range
                if distance > attack_range:
                    self.state = 1
