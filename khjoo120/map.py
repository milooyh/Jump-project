from block import Block
from obstacle import Spike
from portal import Portal

class Map:
    initial_character_x = 50
    initial_character_y = 50
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