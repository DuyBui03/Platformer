from Classes.objects import Block, Fruit, Platform, Fire, Trophy
from Classes.enemy import Slime
from config import WIDTH, HEIGHT, block_size, platform_size

# Hàm tạo sàn (floor)
def create_floor(x_start, y, num, block_size):
    """Tạo một dãy Block làm sàn từ x_start tại vị trí y với số lượng num."""
    return [Block(x_start + i * block_size, HEIGHT - block_size * y, block_size) for i in range(num)]

# Hàm tạo trái cây (fruits)
def create_fruit(x, y, num, width, height, fruit_type):
    """Tạo một dãy Fruit tại vị trí (x, y) với số lượng num và loại fruit_type."""
    return [Fruit(x + i * 100, y, width, height, fruit_type) for i in range(num)]

# Hàm tạo lửa (fire)
def create_fire(x, y, num, block_size):
    """Tạo một dãy Fire tại vị trí (x, y) với số lượng num."""
    return [Fire(x + i * block_size * 2, HEIGHT - block_size - y, 16, 32) for i in range(num)]

# Hàm tạo platform
def create_platform(x, y, num, block_size):
    """Tạo một dãy Block làm platform tại vị trí (x, y) với số lượng num."""
    return [Block(x + i * block_size, HEIGHT - block_size * y, block_size) for i in range(num)]

# Hàm tạo các platform cố định
def create_fixed_platforms():
    """Tạo các platform cố định với kích thước platform_size."""
    platform_width, platform_height = platform_size
    return [
        Platform(600, 400, platform_width, platform_height),
        Platform(400, 400, platform_width, platform_height),
        Platform(900, 300, platform_width, platform_height),
        Platform(100, 700, platform_width, platform_height)
    ]

# Hàm tạo tất cả đối tượng trong game
def create_objects():
    """Tạo và trả về danh sách tất cả đối tượng trong game."""
    # Tạo sàn (floor)
    floor = create_floor(
        x_start=-WIDTH * 3 // block_size, 
        y=1, 
        num=(WIDTH * 6 // block_size), 
        block_size=block_size
    )

    # Tạo các platform
    first_layer_platform = [
        *create_platform(300, 4, 4, block_size),
        *create_platform(-600, 4, 4, block_size),
        *create_platform(-1200, 4, 4, block_size),
        *create_platform(1200, 4, 2, block_size),
        *create_platform(2000, 4, 4, block_size)
    ]
    second_layer_platform = [
        *create_platform(800, 6, 4, block_size),
        *create_platform(1600, 6, 4, block_size)
    ]
    rising_level = [
        *create_platform(100, 2, 1, block_size),
        *create_platform(-100, 2, 1, block_size),
        *create_platform(1200, 2, 1, block_size),
        *create_platform(3000, 3, 3, block_size)
    ]
    fixed_platforms = create_fixed_platforms()
    platforms = first_layer_platform + second_layer_platform + rising_level + fixed_platforms

    # Tạo trái cây (fruits)
    fruits = [
        *create_fruit(320, 370, 4, 30, 30, 'Melon'),
        *create_fruit(-600, 370, 4, 30, 30, 'Bananas'),
        *create_fruit(1200, 370, 2, 30, 30, 'Kiwi')
    ]

    # Tạo lửa (fire)
    floor_fire = [
        *create_fire(200, 64, 6, block_size),
        Fire(100, HEIGHT - block_size - 64, 16, 32),
        Fire(300, HEIGHT - block_size - 64, 16, 32),
        Fire(500, HEIGHT - block_size - 64, 16, 32),
        Fire(700, HEIGHT - block_size - 64, 16, 32)
    ]
    for fire in floor_fire:
        fire.on()  # Kích hoạt lửa

    # Tạo kẻ thù (slime)
    slime = [Slime(250, 645, 44, 30), Slime(500, 645, 44, 30)]

    # Tạo trophy (đặt gần cuối level)
    trophy = Trophy(3100, HEIGHT - block_size * 3, 32, 32)

    # Kết hợp tất cả đối tượng
    objects = floor + platforms + fruits + floor_fire + slime + [trophy]

    return objects