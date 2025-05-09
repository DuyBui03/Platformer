# level.py
from objects import Fire, Cup
from lv1.block_design import create_objects as create_level1_objects
from config import HEIGHT, block_size

class Level:
    def __init__(self, level_id):
        self.level_id = level_id
        self.objects = self.load_objects()

    def load_objects(self):
        if self.level_id == 1:
            objects = create_level1_objects() 
            objects.append(Fire(100, HEIGHT - block_size - 64, 16, 32))
            objects.append(Fire(300, HEIGHT - block_size - 64, 16, 32))
            objects.append(Fire(500, HEIGHT - block_size - 64, 16, 32))
            objects.append(Fire(700, HEIGHT - block_size - 64, 16, 32))
            objects.append(Cup(block_size * 12, HEIGHT - block_size * 8 - block_size, block_size, block_size)) 
            for obj in objects:
                if isinstance(obj, Fire):
                    obj.on()  
            return objects
        else:
            raise ValueError(f"Level {self.level_id} not implemented")

    def get_objects(self):
        return self.objects