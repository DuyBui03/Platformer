# lv1/block_design.py
from objects import Block, Fruits
from config import WIDTH, HEIGHT, block_size

def create_floor():
    return [Block(i * block_size, HEIGHT - block_size, block_size) 
            for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]

def create_platforms():
    return [
        Block(0, HEIGHT - block_size * 2, block_size),
        Block(block_size * 3, HEIGHT - block_size * 4, block_size),
        Block(block_size * 7, HEIGHT - block_size * 6, block_size),
        Block(block_size * 10, HEIGHT - block_size * 3, block_size),
        Block(block_size * 12, HEIGHT - block_size * 8, block_size)
    ]

def create_fruits():
    return [
        Fruits(block_size * 2, HEIGHT - block_size * 3 - block_size, block_size, block_size),  # Trên platform đầu
        Fruits(block_size * 5, HEIGHT - block_size * 5 - block_size, block_size, block_size),  # Trên platform thứ 2
        Fruits(block_size * 8, HEIGHT - block_size * 7 - block_size, block_size, block_size),  # Trên platform thứ 3
        Fruits(block_size * 11, HEIGHT - block_size * 4 - block_size, block_size, block_size)  # Trên platform thứ 4
    ]

def create_objects():
    floor = create_floor()
    platforms = create_platforms()
    fruits = create_fruits()
    for fruit in fruits:
        platforms.append(fruit)
    return floor + platforms