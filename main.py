import pygame
from Classes.player import Player
from Classes.objects import Trophy
from level import Level
from config import WIDTH, HEIGHT, FPS
from sprites import get_background, get_font
from window import show_menu, show_character_selection, show_death_menu
from Functions.load import handle_move
from Functions.button import GameButton
from Classes.audioManager import AudioManager

# Khởi tạo pygame mixer
pygame.mixer.init()
pygame.font.init()

def game_over(window, win, score):
    run = True
    while run:
        if not win:
            window.fill("BLACK")
            menu_text = get_font(55).render("GAME OVER", True, "#d7fcd4")
            menu_rect = menu_text.get_rect(center=(500, 100))
            score_text = get_font(50).render(f'FINAL SCORE: {score}', True, "#d7fcd4")
            score_rect = score_text.get_rect(center=(500, 200))
            
            window.blit(menu_text, menu_rect)
            window.blit(score_text, score_rect)
            pygame.display.update()
        else:
            window.fill("BLACK")
            menu_text = get_font(55).render("YOU WIN!", True, "#d7fcd4")
            menu_rect = menu_text.get_rect(center=(500, 100))
            score_text = get_font(50).render(f'FINAL SCORE: {score}', True, "#d7fcd4")
            score_rect = score_text.get_rect(center=(500, 250))
            
            window.blit(menu_text, menu_rect)
            window.blit(score_text, score_rect)
            pygame.display.update()

def draw(window, background, bg_image, player, objects, offset_x, score_text, buttons, heart_image):
    for tile in background:
        window.blit(bg_image, tile)
    
    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    for button in buttons:
        button.draw(window)
    window.blit(score_text, (150, 15)) 
    
    if heart_image:
        remaining_hearts = player.max_hits - player.fire_hit_count
        for i in range(remaining_hearts):
            window.blit(heart_image, (10 + i * 40, 10))

    pygame.display.update()

def show_win_menu(window, font, alpha, snapshot):
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
    FINAL_SCORE = 0
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PLATFORMER")

    clock = pygame.time.Clock()
    background, bg_image = get_background("Green.png")

    level = Level(2)
    objects = level.get_objects()
    selected_character = "NinjaFrog"
    player = Player(100, 100, 50, 50, selected_character)

    offset_x = 0
    # offset_y = 0
    scroll_area_width = 200
    game_state = "menu"
    
    font = pygame.font.SysFont("arial", 50)
    snapshot = None
    run = True
    pause_key_pressed = False
    is_paused = False 

    audio = AudioManager()

    # Load heart image
    heart_image = None
    try:
        heart_image = pygame.image.load("./assets/Menu/Heart/heart.png")
        heart_image = pygame.transform.scale(heart_image, (32, 32))
    except pygame.error as e:
        print(f"Lỗi khi load hình ảnh heart: {e}")

    # Nút mute/unmute
    try:
        sound_on_img = pygame.image.load("assets/Menu/Buttons/sound.png")
        sound_on_img = pygame.transform.scale(sound_on_img, (32, 32))
        sound_off_img = pygame.image.load("assets/Menu/Buttons/mute.png")
        sound_off_img = pygame.transform.scale(sound_off_img, (32, 32))
        sound_button = GameButton(WIDTH - 80, 5, sound_on_img, 1) 
        settings_img = pygame.image.load("assets/Menu/Buttons/Settings.png")
        settings_img = pygame.transform.scale(settings_img, (32, 32))
        settings_button = GameButton(WIDTH - 40, 5, settings_img, 1)
    except pygame.error as e:
        print(f"Lỗi khi load hình ảnh nút âm thanh: {e}")
        sound_button = None

    while run:
        clock.tick(FPS)
        score_text = get_font(20).render(f'Score:{player.score}', True, "#d7fcd4")
        if game_state == "menu":
            buttons = show_menu(window, font)
            if sound_button:
                sound_button.draw(window)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and not pause_key_pressed:
                        is_paused = not is_paused
                        pause_key_pressed = True
                        if is_paused:
                            audio.pause_music()
                        else:
                            audio.unpause_music()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pause_key_pressed = False
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
                    if sound_button and sound_button.draw(window):
                        audio.toggle_mute()
                        sound_button.image = sound_off_img if audio.is_muted else sound_on_img

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
                            level = Level(2)
                            objects = level.get_objects()
                            offset_x = 0
                            audio.unpause_music()

        elif game_state == "playing":
            audio.unpause_music()
            if not player.alive:
                game_state = "game_over"
                snapshot = window.copy()
                audio.pause_music()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player.jump_count < 2:
                        player.jump()
                    elif event.key == pygame.K_ESCAPE and not pause_key_pressed:
                        is_paused = not is_paused
                        pause_key_pressed = True
                        if is_paused:
                            audio.pause_music()
                        else:
                            audio.unpause_music()
                    elif event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_META:
                        run = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pause_key_pressed = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    if sound_button and sound_button.draw(window):
                        audio.toggle_mute()
                        sound_button.image = sound_off_img if audio.is_muted else sound_on_img
                    if settings_button and settings_button.draw(window):
                        print("Settings button clicked!")
            if not is_paused:
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
                        trophy_rect = obj.rect.move(-offset_x, 0)
                        if player.rect.colliderect(trophy_rect):
                            game_state = "win"
                            snapshot = window.copy()
                            audio.pause_music()
                            break

                # Cập nhật camera
                if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                    (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                    offset_x += player.x_vel
                
                 # Cuộn theo trục y
                # if ((player.rect.top - offset_y <= scroll_area_width) and player.y_vel < 0):  # Nhảy lên, gần rìa trên
                #     offset_y += player.y_vel  # Dịch thế giới xuống (cuộn lên)
                # elif ((player.rect.bottom - offset_y >= HEIGHT - scroll_area_width) and player.y_vel > 0):  # Rơi xuống, gần rìa dưới
                #     offset_y += player.y_vel  # Dịch thế giới lên (cuộn xuống)
                    # offset_x = max(0, min(offset_x, level_width - WIDTH))  # Giới hạn camera

                buttons = [sound_button, settings_button] if sound_button and settings_button else []
                draw(window, background, bg_image, player, objects, offset_x, score_text, buttons, heart_image)
            
            FINAL_SCORE = player.score
            if player.rect.y > 800:
                game_state = "game_over"
                snapshot = window.copy()
                audio.pause_music()

        elif game_state == "game_over":
            audio.pause_music()
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
            audio_del = AudioManager()
            audio.pause_music()
            buttons_win = show_win_menu(window, font, 100, snapshot)

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