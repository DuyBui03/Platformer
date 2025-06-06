# Classes/objects.py

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
    def __init__(self, x, y, width, height, can_move=False):
        super().__init__(x, y, width, height, 'platform')
        platform = get_platform(width, height)
        self.image.blit(platform, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.initial_x = x
        self.speed = 1.2  # Tốc độ cố định cho platform di chuyển
        self.range = 100   # Phạm vi cố định cho platform di chuyển
        self.direction = 1
        self.can_move = can_move

    def move(self):
        if self.can_move:
            self.rect.x += self.speed * self.direction
            if self.rect.x > self.initial_x + self.range:
                self.direction = -1
            elif self.rect.x < self.initial_x - self.range:
                self.direction = 1

    def update(self):
        self.move()


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