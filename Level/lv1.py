import json
from Classes.objects import Block, Platform, Fire, Trophy, Fruit
from Classes.enemy import Slime

def create_objects():
    with open('/Users/duybui/Desktop/Platformer/Level/level1.json', 'r') as f:
        data = json.load(f)
    
    objects = []
    
    # Create Block objects
    for block_data in data['blocks']:
        x = block_data['x']
        y = block_data['y']
        size = block_data['width']
        objects.append(Block(x, y, size))
    
    # Create Platform objects
    for platform_data in data['platforms']:
        x = platform_data['x']
        y = platform_data['y']
        width = platform_data['width']
        height = platform_data['height']
        objects.append(Platform(x, y, width, height))
    
    # Create Fire objects
    for fire_data in data['fire']:
        x = fire_data['x']
        y = fire_data['y']
        width = fire_data['width'] // 2
        height = fire_data['height'] // 2
        objects.append(Fire(x, y, width, height))
    
    # Create Slime (Enemy) objects
    for enemy_data in data['enemies']:
        x = enemy_data['x']
        y = enemy_data['y']
        width = enemy_data['width'] // 2
        height = enemy_data['height'] // 2
        objects.append(Slime(x, y, width, height))
    
    # Create Fruit (Reward) objects
    for reward_data in data['rewards']:
        x = reward_data['x']
        y = reward_data['y']
        width = reward_data['width'] // 2
        height = reward_data['height'] // 2
        fruit_type = 'Apple'  # Hardcoded for simplicity
        objects.append(Fruit(x, y, width, height, fruit_type))
    
    # Create Trophy (Cup) object
    for cup_data in data['cup']:
        x = cup_data['x']
        y = cup_data['y']
        width = cup_data['width'] // 2
        height = cup_data['height'] // 2
        objects.append(Trophy(x, y, width, height))
    
    return objects