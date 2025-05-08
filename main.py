import pygame
from player import Player
from level import Level
from config import WIDTH, HEIGHT, FPS, PLAYER_VEL
from sprites import get_background

def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)
    
    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    
    # Vẽ thanh HP
    pygame.draw.rect(window, (255, 0, 0), (10, 10, 100, 10))  # Nền đỏ
    pygame.draw.rect(window, (0, 255, 0), (10, 10, player.hp, 10))  # Thanh xanh theo HP
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
    for obj in to_check:
        if obj and obj.name == "fire":
            player.take_damage(10)  # Giảm 10 HP khi va chạm với Fire

def show_menu(window):
    window.fill((0, 0, 0))
    font = pygame.font.SysFont("arial", 50)
    text = font.render("Press SPACE to Start", True, (255, 255, 255))
    window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()

def show_game_over(window):
    window.fill((0, 0, 0))
    font = pygame.font.SysFont("arial", 50)
    text = font.render("Game Over! Press R to Restart", True, (255, 255, 255))
    window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PLATFORMER")

    clock = pygame.time.Clock()
    background, bg_image = get_background("Green.png")

    level = Level(1)
    objects = level.get_objects()
    player = Player(100, 100, 50, 50)

    offset_x = 0
    scroll_area_width = 200
    game_state = "menu"

    run = True
    while run:
        clock.tick(FPS)

        if game_state == "menu":
            show_menu(window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = "playing"
                        player = Player(100, 100, 50, 50)  # Reset player
                        offset_x = 0
                    if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_META:
                        run = False
        elif game_state == "playing":
            if not player.alive:
                game_state = "game_over"
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
            show_game_over(window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_state = "playing"
                        player = Player(100, 100, 50, 50)  # Reset player
                        offset_x = 0
                    if event.key == pygame.K_ESCAPE:
                        game_state = "menu"
                    if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_META:
                        run = False

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()