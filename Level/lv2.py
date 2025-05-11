from Classes.objects import Block, Fruit, Platform, Fire, Trophy, MovingPlatform
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

# Hàm tạo platform cố định
def create_platform(x, y, num, block_size):
    """Tạo một dãy Block làm platform tại vị trí (x, y) với số lượng num."""
    return [Block(x + i * block_size, HEIGHT - block_size * y, block_size) for i in range(num)]

# Hàm tạo các platform cố định
def create_fixed_platforms():
    """Tạo các platform cố định với kích thước platform_size."""
    platform_width, platform_height = platform_size
    return [
        Platform(500, HEIGHT - block_size * 5, platform_width, platform_height),
        Platform(1100, HEIGHT - block_size * 6, platform_width, platform_height),
        Platform(200, HEIGHT - block_size * 3, platform_width, platform_height),
    ]

# Hàm tạo platform di chuyển
def create_moving_platforms():
    """Tạo các platform di chuyển với kích thước platform_size và vận tốc."""
    platform_width, platform_height = platform_size
    return [
        MovingPlatform(0, HEIGHT - block_size * 4, platform_width, platform_height, vx=2, x_min=0, x_max=400),
        MovingPlatform(800, HEIGHT - block_size * 3, platform_width, platform_height, vy=1, y_min=HEIGHT - block_size * 5, y_max=HEIGHT - block_size * 3),
        MovingPlatform(1500, HEIGHT - block_size * 4, platform_width, platform_height, vx=3, x_min=1500, x_max=1900),
        # Thêm platform di chuyển mới
        MovingPlatform(2000, HEIGHT - block_size * 5, platform_width, platform_height, vx=2, x_min=2000, x_max=2400),
    ]

# Hàm tạo tất cả đối tượng trong game
def create_objects_lv2():
    """Tạo và trả về danh sách tất cả đối tượng trong Level 2."""
    # Tạo sàn (floor)
    floor = (
        create_floor(x_start=-WIDTH // block_size, y=1, num=8, block_size=block_size) +
        create_floor(x_start=800, y=1, num=6, block_size=block_size) +
        create_floor(x_start=2200, y=1, num=10, block_size=block_size)
    )

    # Tạo các platform cố định
    first_layer_platform = [
        *create_platform(-800, 4, 3, block_size),
        *create_platform(0, 4, 2, block_size),
        *create_platform(1200, 4, 3, block_size),
        *create_platform(1800, 4, 2, block_size),
    ]
    second_layer_platform = [
        *create_platform(-400, 6, 2, block_size),
        *create_platform(600, 6, 3, block_size),
        *create_platform(1400, 6, 2, block_size),
    ]

    # Tạo platform cố định và di chuyển
    fixed_platforms = create_fixed_platforms()
    moving_platforms = create_moving_platforms()
    platforms = first_layer_platform + second_layer_platform + fixed_platforms + moving_platforms

    # Tạo trái cây (fruits)
    fruits = [
        *create_fruit(20, HEIGHT - block_size * 4 - 30, 2, 30, 30, 'Melon'),
        *create_fruit(620, HEIGHT - block_size * 6 - 30, 1, 30, 30, 'Bananas'),
        *create_fruit(1220, HEIGHT - block_size * 4 - 30, 1, 30, 30, 'Kiwi'),
        *create_fruit(2020, HEIGHT - block_size * 5 - 30, 2, 30, 30, 'Cherries'),  # Thêm trái cây mới
    ]

    # Tạo lửa (fire)
    floor_fire = [
        *create_fire(100, 64, 2, block_size),
        *create_fire(850, 64, 2, block_size),
        Fire(10, HEIGHT - block_size * 4 - 32, 16, 32),
        Fire(1410, HEIGHT - block_size * 6 - 32, 16, 32),
        Fire(2020, HEIGHT - block_size * 5 - 32, 16, 32),  # Thêm lửa trên platform mới
    ]
    for fire in floor_fire:
        fire.on()

    # Tạo kẻ thù (slime)
    slime = [
        Slime(120, HEIGHT - block_size - 30, 44, 30),
        Slime(860, HEIGHT - block_size - 30, 44, 30),
        Slime(610, HEIGHT - block_size * 6 - 30, 44, 30),
        Slime(1210, HEIGHT - block_size * 4 - 30, 44, 30),
        Slime(2020, HEIGHT - block_size * 5 - 30, 44, 30),  # Thêm slime trên platform mới
    ]

    # Tạo trophy
    trophy = Trophy(2500, HEIGHT - block_size * 4, 32, 32)

    # Kết hợp tất cả đối tượng
    objects = floor + platforms + fruits + floor_fire + slime + [trophy]

    return objects