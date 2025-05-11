import pygame
from Classes.player import Player
from Classes.objects import Trophy
from level import Level
from config import WIDTH, HEIGHT, FPS, PLAYER_VEL
from sprites import get_background
from window import show_menu, show_character_selection, show_death_menu
from Functions.load import handle_move

def draw(window, background, bg_image, player, objects, offset_x):
    """Vẽ tất cả đối tượng lên màn hình."""
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

def show_win_menu(window, font, alpha, snapshot):
    """Hiển thị màn hình chiến thắng."""
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(alpha)
    window.blit(snapshot, (0, 0))
    window.blit(overlay, (0, 0))

    win_text = font.render("You Win!", True, (255, 255, 255))
    win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    window.blit(win_text, win_rect)

    buttons = [
        ("restart", pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)),
        ("exit", pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50))
    ]
    for name, rect in buttons:
        pygame.draw.rect(window, (100, 100, 100), rect)
        text = font.render(name.capitalize(), True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        window.blit(text, text_rect)

    pygame.display.update()
    return buttons

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
    level_width = WIDTH * 6  # Giả định level rộng gấp 6 lần màn hình
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
            font_char = pygame.font.SysFont("arial", 30)
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
                    try:
                        obj.loop(objects)
                    except TypeError:
                        obj.loop()

            handle_move(player, objects)

            # Kiểm tra va chạm với Trophy
            for obj in objects:
                if isinstance(obj, Trophy):
                    # Use obj.rect directly, adjusted for camera offset
                    trophy_rect = obj.rect.move(-offset_x, 0)
                    if player.rect.colliderect(trophy_rect):
                        game_state = "win"
                        snapshot = window.copy()
                        break

            draw(window, background, bg_image, player, objects, offset_x)

            # Cập nhật camera
            if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                offset_x += player.x_vel
                # Giới hạn camera
                offset_x = max(-level_width // 2, min(offset_x, level_width // 2 - WIDTH))

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
        elif game_state == "win":
            buttons_win = show_win_menu(window, font, 100, snapshot)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    for name, rect in buttons_win:
                        if rect.collidepoint(pos):
                            if name == "restart":
                                game_state = "character_select"
                            elif name == "exit":
                                run = False

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()