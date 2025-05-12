import pygame
from config import WIDTH, HEIGHT
from sprites import load_sprite_sheets, get_background

BTN_W, BTN_H = 200, 50
BTN_SPACING = 20
SHADOW_OFFSET = 4

def draw_rounded_rect(surface, rect, color, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_gradient(surface, rect, top_color, bottom_color):
    x, y, w, h = rect
    for i in range(h):
        ratio = i / h
        r = top_color[0] + (bottom_color[0] - top_color[0]) * ratio
        g = top_color[1] + (bottom_color[1] - top_color[1]) * ratio
        b = top_color[2] + (bottom_color[2] - top_color[2]) * ratio
        pygame.draw.line(surface, (int(r), int(g), int(b)), (x, y+i), (x+w, y+i))

def show_menu(window, font):
    background, bg_image = get_background("Green.png")
    for tile in background:
        window.blit(bg_image, tile)
    
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((20, 20, 40, 200))
    window.blit(overlay, (0, 0))

    titles = ["Play", "Point", "Exit"]
    buttons = []
    total_height = len(titles) * BTN_H + (len(titles)-1) * BTN_SPACING
    start_y = HEIGHT//2 - total_height//2

    mx, my = pygame.mouse.get_pos()
    for i, title in enumerate(titles):
        x = WIDTH//2 - BTN_W//2
        y = start_y + i*(BTN_H + BTN_SPACING)
        rect = pygame.Rect(x, y, BTN_W, BTN_H)
        shadow_rect = rect.move(SHADOW_OFFSET, SHADOW_OFFSET)
        draw_rounded_rect(window, shadow_rect, (0, 0, 0, 80), radius=10)
        if rect.collidepoint((mx, my)):
            top_col = (100, 180, 240)
            bot_col = (70, 120, 200)
        else:
            top_col = (120, 200, 255)
            bot_col = (70, 130, 180)
        draw_gradient(window, rect, top_col, bot_col)
        pygame.draw.rect(window, (255,255,255, 50), rect, width=2, border_radius=10)
        text_surf = font.render(title, True, (255,255,255))
        window.blit(
            text_surf,
            (x + (BTN_W-text_surf.get_width())//2,
             y + (BTN_H-text_surf.get_height())//2)
        )
        buttons.append((title.lower(), rect))

    pygame.display.update()
    return buttons

def show_level_selection(window, font):
    background, bg_image = get_background("Green.png")
    for tile in background:
        window.blit(bg_image, tile)
    
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((20, 20, 40, 200))
    window.blit(overlay, (0, 0))

    title_surf = font.render("Select a Level", True, (255, 255, 255))
    title_rect = title_surf.get_rect(center=(WIDTH//2, 50))
    shadow_rect = title_rect.move(2, 2)
    draw_rounded_rect(window, shadow_rect, (0, 0, 0, 80), radius=10)
    window.blit(title_surf, title_rect)


    levels = ["Level 1", "Level 2", "Level 3"]
    buttons = []
    total_height = len(levels) * BTN_H + (len(levels)-1) * BTN_SPACING
    start_y = HEIGHT//2 - total_height//2

    mx, my = pygame.mouse.get_pos()
    for i, level in enumerate(levels):
        x = WIDTH//2 - BTN_W//2
        y = start_y + i*(BTN_H + BTN_SPACING)
        rect = pygame.Rect(x, y, BTN_W, BTN_H)
        shadow_rect = rect.move(SHADOW_OFFSET, SHADOW_OFFSET)
        draw_rounded_rect(window, shadow_rect, (0, 0, 0, 80), radius=10)
        if rect.collidepoint((mx, my)):
            top_col = (100, 180, 240)
            bot_col = (70, 120, 200)
        else:
            top_col = (120, 200, 255)
            bot_col = (70, 130, 180)
        draw_gradient(window, rect, top_col, bot_col)
        pygame.draw.rect(window, (255,255,255, 50), rect, width=2, border_radius=10)
        text_surf = font.render(level, True, (255,255,255))
        window.blit(
            text_surf,
            (x + (BTN_W-text_surf.get_width())//2,
             y + (BTN_H-text_surf.get_height())//2)
        )
        buttons.append((level.lower(), rect))

    pygame.display.update()
    return buttons

def show_character_selection(window, font):
    background, bg_image = get_background("Green.png")
    for tile in background:
        window.blit(bg_image, tile)
    
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((20, 20, 40, 200))
    window.blit(overlay, (0, 0))

    characters = ["NinjaFrog", "MaskDude", "PinkMan", "KenCarson"]
    buttons = []
    char_width, char_height = 80, 80
    spacing = 50
    total_width = len(characters) * char_width + (len(characters)-1) * spacing
    start_x = WIDTH//2 - total_width//2
    y = HEIGHT//2 - char_height//2

    mx, my = pygame.mouse.get_pos()
    title_surf = font.render("Choose your character", True, (255, 255, 255))
    title_rect = title_surf.get_rect(center=(WIDTH//2, 50))
    shadow_rect = title_rect.move(2, 2)
    draw_rounded_rect(window, shadow_rect, (0, 0, 0, 80), radius=10)
    window.blit(title_surf, title_rect)

    for i, char in enumerate(characters):
        sprites = load_sprite_sheets("MainCharacters", char, 32, 32, True)  # Sử dụng cache
        preview = sprites["idle_right"][0]
        bounding_rect = preview.get_bounding_rect()
        trimmed_surface = pygame.Surface((bounding_rect.width, bounding_rect.height), pygame.SRCALPHA)
        trimmed_surface.blit(preview, (0, 0), bounding_rect)
        scale_factor = min(char_width * 0.8 / bounding_rect.width, char_height * 0.8 / bounding_rect.height)
        preview = pygame.transform.smoothscale(trimmed_surface, (int(bounding_rect.width * scale_factor), int(bounding_rect.height * scale_factor)))
        
        x = start_x + i * (char_width + spacing)
        rect = pygame.Rect(x, y, char_width, char_height)
        
        preview_rect = preview.get_rect(center=rect.center)
        window.blit(preview, preview_rect)
        text_surf = font.render(char, True, (255,255,255))
        window.blit(text_surf, (x + (char_width-text_surf.get_width())//2, y + char_height + 10))
        
        if rect.collidepoint((mx, my)):
            glow_width = 4
            glow_rect = preview_rect.inflate(glow_width * 2, glow_width * 2)
            glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            alpha = (pygame.time.get_ticks() // 200 % 2) * 100 + 100
            pygame.draw.rect(glow_surface, (0, 255, 255, alpha), glow_surface.get_rect(), border_radius=5)
            window.blit(glow_surface, glow_rect.topleft, special_flags=pygame.BLEND_RGB_ADD)
        
        buttons.append((char, rect))

    pygame.display.update()
    return buttons

def show_death_menu(window, font, score, bg_snapshot):
    BTN_SIZE = 64
    window.blit(bg_snapshot, (0,0))
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0, 150))  
    window.blit(overlay, (0,0))

    score_surf = font.render(f"Score: {score}", True, (255, 215, 0))
    window.blit(score_surf, (WIDTH//2 - score_surf.get_width()//2, HEIGHT//2 - 150))

    icons = {
        "restart": pygame.image.load("assets/Menu/Buttons/Restart.png").convert_alpha(),
        "menu":  pygame.image.load("assets/Menu/Buttons/menu.jpg").convert_alpha(),
        "exit":    pygame.image.load("assets/Menu/Buttons/Close.png").convert_alpha(),
    }

    total_w = 3 * BTN_SIZE
    start_x = WIDTH//2 - total_w//2
    y = HEIGHT//2 - BTN_SIZE//2

    buttons = []
    for i, name in enumerate(["restart", "menu", "exit"]):
        x = start_x + i * BTN_SIZE
        ico = pygame.transform.smoothscale(icons[name], (BTN_SIZE, BTN_SIZE))
        ico_rect = ico.get_rect(topleft=(x, y))
        window.blit(ico, ico_rect)
        buttons.append((name, ico_rect))

    pygame.display.update()
    return buttons

def show_settings(window, font, bg_snapshot):
    BTN_SIZE = 64
    window.blit(bg_snapshot, (0, 0))
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    window.blit(overlay, (0, 0))

    title_surf = font.render("Settings", True, (255, 255, 255))
    window.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, HEIGHT//2 - 150))

    icons = {
        "continue": pygame.image.load("assets/Menu/Buttons/Play.png").convert_alpha(),
        "menu": pygame.image.load("assets/Menu/Buttons/menu.jpg").convert_alpha(),
    }

    total_w = 2 * BTN_SIZE
    start_x = WIDTH//2 - total_w//2
    y = HEIGHT//2 - BTN_SIZE//2

    buttons = []
    for i, name in enumerate(["continue", "menu"]):
        x = start_x + i * BTN_SIZE
        ico = pygame.transform.smoothscale(icons[name], (BTN_SIZE, BTN_SIZE))
        ico_rect = ico.get_rect(topleft=(x, y))
        window.blit(ico, ico_rect)
        buttons.append((name, ico_rect))

    pygame.display.update()
    return buttons
def show_high_scores(window, font, high_scores):
    background, bg_image = get_background("Green.png")
    for tile in background:
        window.blit(bg_image, tile)
    
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((20, 20, 40, 200))
    window.blit(overlay, (0, 0))

    title_surf = font.render("High Scores", True, (255, 255, 255))
    title_rect = title_surf.get_rect(center=(WIDTH//2, 50))
    shadow_rect = title_rect.move(2, 2)
    draw_rounded_rect(window, shadow_rect, (0, 0, 0, 80), radius=10)
    window.blit(title_surf, title_rect)

    levels = ["Level 1", "Level 2", "Level 3"]
    score_displays = []
    total_height = len(levels) * BTN_H + BTN_H + BTN_SPACING * (len(levels))
    start_y = HEIGHT//2 - total_height//2

    mx, my = pygame.mouse.get_pos()
    for i, level in enumerate(levels):
        x = WIDTH//2 - BTN_W//2
        y = start_y + i * (BTN_H + BTN_SPACING)
        rect = pygame.Rect(x, y, BTN_W, BTN_H)
        draw_rounded_rect(window, rect.move(SHADOW_OFFSET, SHADOW_OFFSET), (0, 0, 0, 80), radius=10)
        draw_gradient(window, rect, (120, 200, 255), (70, 130, 180))
        pygame.draw.rect(window, (255,255,255, 50), rect, width=2, border_radius=10)
        score = high_scores.get(f"level_{i+1}", 0)
        text_surf = font.render(f"{level}: {score}", True, (255,255,255))
        window.blit(
            text_surf,
            (x + (BTN_W-text_surf.get_width())//2,
             y + (BTN_H-text_surf.get_height())//2)
        )
        score_displays.append((level.lower(), rect))

    # Back button
    back_rect = pygame.Rect(WIDTH//2 - BTN_W//2, start_y + len(levels) * (BTN_H + BTN_SPACING), BTN_W, BTN_H)
    draw_rounded_rect(window, back_rect.move(SHADOW_OFFSET, SHADOW_OFFSET), (0, 0, 0, 80), radius=10)
    if back_rect.collidepoint((mx, my)):
        top_col = (100, 180, 240)
        bot_col = (70, 120, 200)
    else:
        top_col = (120, 200, 255)
        bot_col = (70, 130, 180)
    draw_gradient(window, back_rect, top_col, bot_col)
    pygame.draw.rect(window, (255,255,255, 50), back_rect, width=2, border_radius=10)
    back_text = font.render("Back", True, (255,255,255))
    window.blit(
        back_text,
        (back_rect.x + (BTN_W-back_text.get_width())//2,
         back_rect.y + (BTN_H-back_text.get_height())//2)
    )

    pygame.display.update()
    return [("back", back_rect)]   

def show_win_menu(window, font, alpha, snapshot):
    window.blit(snapshot, (0, 0))
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(alpha)
    window.blit(overlay, (0, 0))

    title_surf = font.render("You Win!", True, (255, 255, 255))
    title_rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 150))
    window.blit(title_surf, title_rect)

    buttons = ["restart", "menu", "exit"]
    button_rects = []
    total_height = len(buttons) * BTN_H + (len(buttons)-1) * BTN_SPACING
    start_y = HEIGHT//2 - total_height//2 + 50

    mx, my = pygame.mouse.get_pos()
    for i, name in enumerate(buttons):
        x = WIDTH//2 - BTN_W//2
        y = start_y + i * (BTN_H + BTN_SPACING)
        rect = pygame.Rect(x, y, BTN_W, BTN_H)
        shadow_rect = rect.move(SHADOW_OFFSET, SHADOW_OFFSET)
        draw_rounded_rect(window, shadow_rect, (0, 0, 0, 80), radius=10)
        if rect.collidepoint((mx, my)):
            top_col = (100, 180, 240)
            bot_col = (70, 120, 200)
        else:
            top_col = (120, 200, 255)
            bot_col = (70, 130, 180)
        draw_gradient(window, rect, top_col, bot_col)
        pygame.draw.rect(window, (255,255,255, 50), rect, width=2, border_radius=10)
        text_surf = font.render(name.capitalize(), True, (255,255,255))
        window.blit(
            text_surf,
            (x + (BTN_W-text_surf.get_width())//2,
             y + (BTN_H-text_surf.get_height())//2)
        )
        button_rects.append((name, rect))

    pygame.display.update()
    return button_rects