import pygame
from config import PLAYER_VEL, GRAVITY
from sprites import load_sprite_sheets

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
                collided_objects.append(obj)
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
                collided_objects.append(obj)
    return collided_objects

def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
    player.move(-dx, 0)
    player.update()
    return collided_object

def handle_move(player, objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    
    fire_collided = None
    for obj in to_check:
        if obj and obj.name == "fire":
            fire_collided = obj
            break
        if obj and obj.name == "fruit":
            player.score += 100
            objects.remove(obj)
            break
    if fire_collided and fire_collided != player.current_fire and not player.is_invincible:
        player.take_damage()
        player.current_fire = fire_collided
    elif not fire_collided:
        player.current_fire = None
    
       