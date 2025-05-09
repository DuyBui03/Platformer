import pygame
from player import Player
from level import Level
from config import WIDTH, HEIGHT, FPS, PLAYER_VEL
from sprites import get_background
from window import show_menu, show_character_selection, show_death_menu    

def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)
    
    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    
    heart_image = pygame.image.load("./assets/Menu/Heart/heart.png")
    heart_image = pygame.transform.scale(heart_image, (32, 32))
    remaining_hearts = player.max_hits - player.fire_hit_count
    for i in range(remaining_hearts):
        window.blit(heart_image, (10 + i * 40, 10))

    pygame.display.update()

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
    if fire_collided and fire_collided != player.current_fire and not player.is_invincible:
        player.take_damage()
        player.current_fire = fire_collided
    elif not fire_collided:
        player.current_fire = None
        
def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PLATFORMER")

    clock = pygame.time.Clock()
    background, bg_image = get_background("Green.png")

    level = Level(1)
    objects = level.get_objects()
    selected_character = "NinjaFrog"  # Mặc định
    player = Player(100, 100, 50, 50, selected_character)

    offset_x = 0
    scroll_area_width = 200
    game_state = "menu"
    
    font = pygame.font.SysFont("arial", 50)
    snapshot = None 
    run = True
    while run:
        clock.tick(FPS)

        if game_state == "menu":
            buttons = show_menu(window, font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    for name, rect in buttons:
                        if rect.collidepoint(pos):
                            if name == "play":
                                game_state = "character_select"
                            elif name == "point":
                                game_state = "score"
                            elif name == "exit":
                                run = False
        elif game_state == "character_select":
            font_char = pygame.font.SysFont("arial", 0)
            buttons = show_character_selection(window, font_char)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    for char, rect in buttons:
                        if rect.collidepoint(pos):
                            selected_character = char
                            game_state = "playing"
                            player = Player(100, 100, 50, 50, selected_character)
                            level = Level(1)
                            objects = level.get_objects()
                            offset_x = 0
        elif game_state == "playing":
            if not player.alive:
                game_state = "game_over"
                snapshot = window.copy()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player.jump_count < 2:
                        player.jump()
                    if event.key == pygame.K_ESCAPE:
                        game_state = "menu"
                    if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_META:
                        run = False

            player.loop(FPS)
            for obj in objects:
                if hasattr(obj, "loop"):
                    obj.loop()
            handle_move(player, objects)
            draw(window, background, bg_image, player, objects, offset_x)

            if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                offset_x += player.x_vel
        elif game_state == "game_over":
            buttons_over = show_death_menu(window, font, 100, snapshot)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    for name, rect in buttons_over:
                        if rect.collidepoint(pos):
                            if name == "restart":
                                game_state = "character_select"
                            elif name == "exit":
                                run = False

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()