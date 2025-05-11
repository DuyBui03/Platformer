import pygame
class AudioManager:
    def __init__(self):
        self.music_file = "assets/music/funny.mp3"  # File music
        self.is_muted = False
        self.default_volume = 0.5

        # Load music
        try:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.set_volume(self.default_volume)
            pygame.mixer.music.play(-1)  # Loop vô hạn
        except pygame.error as e:
            print(f"Lỗi khi load music: {e}")

    def toggle_mute(self):
        """Bật/tắt âm thanh"""
        self.is_muted = not self.is_muted
        volume = 0 if self.is_muted else self.default_volume
        pygame.mixer.music.set_volume(volume)

    def pause_music(self):
        """Tạm dừng music"""
        pygame.mixer.music.pause()

    def unpause_music(self):
        """Tiếp tục music"""
        if not self.is_muted:
            pygame.mixer.music.unpause()