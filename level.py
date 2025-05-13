from Level.lv1 import create_objects
from Level.level_2 import create_objects as create_objects_lv2
class Level:
    def __init__(self, level_id):
        self.level_id = level_id
        self.objects = self.load_objects()

    def load_objects(self):
        """Tải danh sách đối tượng cho level dựa trên level_id."""
        try:
            if self.level_id == 1:
                return create_objects()
            elif self.level_id == 2:
                return create_objects_lv2()
            else:
                raise ValueError(f"Level {self.level_id} not implemented")
        except Exception as e:
            print(f"Error loading level {self.level_id}: {e}")
            return []

    def get_objects(self):
        """Trả về danh sách đối tượng của level."""
        return self.objects

    def reset(self):
        """Tải lại các đối tượng của level."""
        self.objects = self.load_objects()