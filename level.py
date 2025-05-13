from Level.level import create_objects
import os
class Level:
    def __init__(self, level_id):
        self.level_id = level_id
        self.objects = self.load_objects()

    def load_objects(self):
        """Tải danh sách đối tượng cho level dựa trên level_id."""
        # Lấy đường dẫn thư mục của tệp Python hiện tại
        current_dir = os.path.dirname(os.path.abspath(__file__))

        PATH_1 = os.path.join(current_dir, 'Level', 'JsonLevel', 'level_1.json')
        PATH_2 = os.path.join(current_dir, 'Level', 'JsonLevel', 'level_2.json')
        PATH_3 = os.path.join(current_dir, 'Level', 'JsonLevel', 'level_3.json')
        PATH_4 = os.path.join(current_dir, 'Level', 'JsonLevel', 'level_4.json')

        # PATH_4 = r'C:\Users\longc\project\Platformer\Level\JsonLevel\level4.json'
        try:
            if self.level_id == 1:
                return create_objects(PATH_1)
            elif self.level_id == 2:
                return create_objects(PATH_2)
            elif self.level_id == 3:
                return create_objects(PATH_3)
            elif self.level_id == 4:
                return create_objects(PATH_4)
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