from block import Block, MovingBlock
from obstacle import Spike
from portal import Portal

class Map1:
    initial_character_x = 100
    initial_character_y = 500
    blocks = [  
        Block(100, 500),
        Block(300, 400),
        Block(500, 300),
        Block(700, 200)
    ]
    portals = [
        Portal(745, 50, 40, 40, 'stage2')
    ]

class Map2:
    initial_character_x = 50
    initial_character_y = 100
    blocks = [
        Block(50, 100),
        Block(250, 400),
        Block(500, 300),
        Block(600, 200)
    ]
    portals = [
        Portal(745, 50, 40, 40, 'stage3')
    ]

class Map3:
    initial_character_x = 0
    initial_character_y = 300
    blocks = [
        Block(0, 300),
        Block(100, 300),
        Block(200, 300),
        Block(300, 300),
        Block(400, 300),
        Block(500, 300),
        Block(600, 300),
        Block(700, 300)
    ]
    spikes = [
        Spike(150, 270),
        Spike(225, 150),
        Spike(300, 270),
        Spike(375, 150),
        Spike(450, 270),
        Spike(525, 150),
        Spike(600, 270),
        Spike(675, 150)
    ]
    portals = [
        Portal(745, 200, 40, 40, 'stage4')
    ]

class Map4:
    initial_character_x = 0
    initial_character_y = 550
    blocks = [
        Block(0, 550),
        MovingBlock(400, 525, move_range=200, speed=2),
        Block(700, 425),
        MovingBlock(400, 300, move_range=200, speed=3),
        Block(0, 200),
        MovingBlock(400, 100, move_range=200, speed=4)
    ]
    portals = [
        Portal(745, 50, 40, 40, 'stage5')
    ]

maps = [Map1, Map2, Map3, Map4]
