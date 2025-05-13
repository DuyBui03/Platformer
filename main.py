import json
import os
import pygame
from Classes.player import Player
from Classes.objects import Trophy, Fruit
from level import Level
from config import WIDTH, HEIGHT, FPS
from sprites import get_background, get_font
from window import show_menu, show_character_selection, show_level_selection, show_death_menu, show_settings, show_high_scores, show_win_menu
from Functions.load import handle_move
from Functions.button import GameButton
from Classes.audioManager import AudioManager

pygame.mixer.init()
pygame.font.init()

def load_high_scores():
    """Load high scores from a JSON file, return a dictionary."""
    try:
        if os.path.exists("high_scores.json"):
            with open("high_scores.json", "r") as f:
                return json.load(f)
        else:
            return {"level_1": 0, "level_2": 0, "level_3": 0}
    except Exception as e:
        print(f"Error loading high scores: {e}")
        return {"level_1": 0, "level_2": 0, "level_3": 0}

def save_high_scores(high_scores):
    """Save high scores to a JSON file."""
    try:
        with open("high_scores.json", "w") as f:
            json.dump(high_scores, f, indent=4)
    except Exception as e:
        print(f"Error saving high scores: {e}")

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

def reset_player_state(selected_character):
    """Reset player's state for a new game."""
    return Player(100, 100, 50, 50, selected_character)

def main():
    FINAL_SCORE = 0
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PLATFORMER")

    clock = pygame.time.Clock()
    high_scores = load_high_scores()
    background, bg_image = get_background("Green.png")

    selected_level = 1
    level = Level(selected_level)
    objects = level.get_objects()
    selected_character = "NinjaFrog"
    player = Player(100, 100, 50, 50, selected_character)

    offset_x = 0
    scroll_area_width = 200
    game_state = "menu"
    
    font = pygame.font.SysFont("arial", 50)
    snapshot = None
    run = True
    pause_key_pressed = False
    is_paused = False 

    audio = AudioManager()

    heart_image = None
    try:
        heart_image = pygame.image.load("./assets/Menu/Heart/heart.png")
        heart_image = pygame.transform.scale(heart_image, (32, 32))
    except pygame.error as e:
        print(f"Lỗi khi load hình ảnh heart: {e}")

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
                                game_state = "level_select"
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
                            level = Level(selected_level)
                            objects = level.get_objects()
                            offset_x = 0
                            audio.unpause_music()
                            
        elif game_state == "level_select":
            font_level = pygame.font.SysFont("arial", 30)
            buttons = show_level_selection(window, font_level)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    for level_name, rect in buttons:
                        if rect.collidepoint(pos):
                            if level_name == "level 1":
                                selected_level = 1
                            elif level_name == "level 2":
                                selected_level = 2
                            elif level_name == "level 3":
                                selected_level = 3
                            elif level_name == "level 4":
                                selected_level = 4
                            game_state = "character_select"
                            audio.unpause_music()

        elif game_state == "playing":
            audio.unpause_music()
            if not player.alive:
                game_state = "game_over"
                snapshot = window.copy()
                audio.pause_music()
                # Update high score
                level_key = f"level_{selected_level}"
                if player.score > high_scores.get(level_key, 0):
                    high_scores[level_key] = player.score
                    save_high_scores(high_scores)
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
                        snapshot = window.copy()
                        game_state = "settings"

            if not is_paused:
                player.loop(FPS)
                for obj in objects:
                    print(f"Object: {obj.name}, Position: {obj.rect.topleft}")
                    if hasattr(obj, "loop"):
                        try:
                            obj.loop(objects)
                        except TypeError:
                            obj.loop()
                    if hasattr(obj, "update"):
                        obj.update() # Thêm dòng này để gọi update cho tất cả các đối tượng có phương thức update

                handle_move(player, objects)
                if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                    (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                    offset_x += player.x_vel

                buttons = [sound_button, settings_button] if sound_button and settings_button else []
                draw(window, background, bg_image, player, objects, offset_x, score_text, buttons, heart_image)

            FINAL_SCORE = player.score
            if player.rect.y > 800:
                game_state = "game_over"
                snapshot = window.copy()
                audio.pause_music()
                # Update high score
                level_key = f"level_{selected_level}"
                if player.score > high_scores.get(level_key, 0):
                    high_scores[level_key] = player.score
                    save_high_scores(high_scores)
            if player.level_completed:
                game_state = "win"
                snapshot = window.copy()
                audio.pause_music()
                level_key = f"level_{selected_level}"
                if player.score > high_scores.get(level_key, 0):
                    high_scores[level_key] = player.score
                    save_high_scores(high_scores)
                
        elif game_state == "settings":
            buttons_settings = show_settings(window, font, snapshot)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    for name, rect in buttons_settings:
                        if rect.collidepoint(pos):
                            if name == "continue":
                                game_state = "playing"
                                audio.unpause_music()
                            elif name == "menu":
                                game_state = "menu"

        elif game_state == "score":
            font_score = pygame.font.SysFont("arial", 20)
            buttons = show_high_scores(window, font_score, high_scores)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    for name, rect in buttons:
                        if rect.collidepoint(pos):
                            if name == "back":
                                game_state = "menu"

        elif game_state == "game_over":
            audio.pause_music()
            buttons_over = show_death_menu(window, font, FINAL_SCORE, snapshot)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    for name, rect in buttons_over:
                        if rect.collidepoint(pos):
                            if name == "restart":
                                game_state = "level_select"  # Return to level select
                                player = reset_player_state(selected_character)  # Reset player state
                            elif name == "menu":
                                game_state = "menu"
                                player = reset_player_state(selected_character)  # Reset player state
                            elif name == "exit":
                                run = False

        elif game_state == "win":
            buttons_win = show_win_menu(window, font, player.score, snapshot)  # Use player's actual score
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    for name, rect in buttons_win:
                        if rect.collidepoint(pos):
                            if name == "restart":
                                game_state = "level_select"  # Return to level select
                                player = reset_player_state(selected_character)  # Reset player state
                            elif name == "menu":
                                game_state = "menu"
                                player = reset_player_state(selected_character)  # Reset player state
                            elif name == "exit":
                                run = False

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()