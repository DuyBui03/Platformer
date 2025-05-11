import pygame
from sprites import load_sprite_sheets, flip
from config import PLAYER_VEL, GRAVITY, ANIMATION_DELAY

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, character="NinjaFrog"):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.fire_hit_count = 0
        self.max_hits = 3
        self.alive = True
        self.last_damage_time = 0
        self.damage_cooldown = 500
        self.current_fire = None
        self.is_invincible = False
        self.invincibility_end_time = 0
        self.flash_timer = 0
        self.character = character
        self.SPRITES = load_sprite_sheets("MainCharacters", self.character, 32, 32, True)
        self.score = 0
        if not self.SPRITES:
            raise ValueError(f"Failed to load sprites for character: {character}")

    def jump(self):
        if self.alive:
            self.y_vel = -GRAVITY * 8
            self.animation_count = 0 
            self.jump_count += 1
            if self.jump_count == 1:
                self.fall_count = 0

    def take_damage(self):
        current_time = pygame.time.get_ticks()
        if self.alive and not self.is_invincible and current_time - self.last_damage_time >= self.damage_cooldown:
            self.fire_hit_count += 1
            self.last_damage_time = current_time
            self.is_invincible = True
            self.invincibility_end_time = current_time + 3000
            self.make_hit()
            if self.fire_hit_count >= self.max_hits:
                self.alive = False

    def make_hit(self):
        if not self.is_invincible:
            self.hit = True

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        if self.alive:
            self.x_vel = -vel
            if self.direction != "left":
                self.direction = "left"
                self.animation_count = 0

    def move_right(self, vel):
        if self.alive:
            self.x_vel = vel
            if self.direction != "right":
                self.direction = "right"
                self.animation_count = 0

    def loop(self, fps):
        if self.alive:
            self.y_vel += min(1, (self.fall_count / fps) * GRAVITY)
            self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0     

        current_time = pygame.time.get_ticks()
        if self.is_invincible and current_time >= self.invincibility_end_time:
            self.is_invincible = False
            self.flash_timer = 0

        if self.is_invincible:
            self.flash_timer += 1

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"        
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES.get(sprite_sheet_name, self.SPRITES["idle_right"])
        sprite_index = (self.animation_count // ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        if not self.is_invincible or (self.flash_timer % 6 < 3):
            win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))