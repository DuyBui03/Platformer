# game_objects.py

import pygame
from sprites import get_block, load_sprite_sheets, get_platform

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y ))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Platform(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        platform = get_platform(width, height)
        self.image.blit(platform, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Fire(Object):
    ANIMATION_DELAY = 3
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0
            
class Trophy(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, 'trophy')
        self.image = pygame.image.load('assets/Items/Checkpoints/End/End (Idle).png')
        self.mask = pygame.mask.from_surface(self.image)

class Fruit(Object):
    def __init__(self, x, y, width, height, fruit_type):
        super().__init__(x, y, width, height, 'fruit')
        self.fruit = load_sprite_sheets('Items', 'Fruits', width, height)
        self.image = self.fruit[fruit_type][0]
        self.mask = pygame.mask.from_surface(self.image)

# Lớp MovingPlatform kế thừa Platform để hỗ trợ di chuyển
class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, vx=0, vy=0, x_min=None, x_max=None, y_min=None, y_max=None):
        super().__init__(x, y, width, height)
        self.vx = vx
        self.vy = vy
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def loop(self):
        """Cập nhật vị trí platform và đảo chiều khi chạm giới hạn."""
        self.rect.x += self.vx
        self.rect.y += self.vy
        # Đảo chiều khi chạm x_min/x_max
        if self.x_min is not None and self.rect.x <= self.x_min:
            self.rect.x = self.x_min
            self.vx = -self.vx
        if self.x_max is not None and self.rect.x >= self.x_max - self.rect.width:
            self.rect.x = self.x_max - self.rect.width
            self.vx = -self.vx
        # Đảo chiều khi chạm y_min/y_max
        if self.y_min is not None and self.rect.y <= self.y_min:
            self.rect.y = self.y_min
            self.vy = -self.vy
        if self.y_max is not None and self.rect.y >= self.y_max - self.rect.height:
            self.rect.y = self.y_max - self.rect.height
            self.vy = -self.vy