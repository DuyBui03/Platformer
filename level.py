# level.py
from objects import Fire
from lv1.block_design import create_objects as create_level1_objects
from config import HEIGHT, block_size

class Level:
    def __init__(self, level_id):
        self.level_id = level_id
        self.objects = self.load_objects()

    def load_objects(self):
        """Tải các đối tượng cho màn chơi dựa trên level_id."""
        if self.level_id == 1:
            objects = create_level1_objects()  # Lấy objects từ block_design.py
            # Thêm bẫy Fire vào màn chơi
            objects.append(Fire(100, HEIGHT - block_size - 64, 16, 32))
            objects.append(Fire(300, HEIGHT - block_size - 64, 16, 32))
            for obj in objects:
                if isinstance(obj, Fire):
                    obj.on()  # Bật hoạt hình cho Fire
            return objects
        else:
            raise ValueError(f"Level {self.level_id} not implemented")

    def get_objects(self):
        """Trả về danh sách các đối tượng trong màn chơi."""
        return self.objects