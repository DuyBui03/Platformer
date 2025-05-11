from Classes.objects import Fire
from config import HEIGHT, block_size
from Level.lv1 import create_objects

class Level:
    def __init__(self, level_id):
        self.level_id = level_id
        self.objects = self.load_objects()

    def load_objects(self):
        """Tải danh sách đối tượng cho level dựa trên level_id."""
        if self.level_id == 1:
            return create_objects()
        else:
            raise ValueError(f"Level {self.level_id} not implemented")

    def get_objects(self):
        """Trả về danh sách đối tượng của level."""
        return self.objects