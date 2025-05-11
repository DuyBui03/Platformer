import pygame

def load_music(file_path):
    """Load background music."""
    try:
        pygame.mixer.music.load(file_path)
        return True
    except pygame.error as e:
        print(f"Failed to load music {file_path}: {e}")
        return False

def load_sound_effect(file_path):
    """Load a sound effect."""
    try:
        sound = pygame.mixer.Sound(file_path)
        return sound
    except pygame.error as e:
        print(f"Failed to load sound effect {file_path}: {e}")
        return None