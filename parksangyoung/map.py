from block import Block, MovingBlock
from obstacle import Spike

class Map1:

    blocks = [  
        Block(100, 500),
        Block(300, 400),
        Block(500, 300),
        Block(700, 200)
        ]

class Map2:

    blocks = [
        Block(50, 100),
        Block(250, 400),
        Block(500, 300),
        Block(600, 200)
        ]

class Map3:

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
        Spike(150, 250,),
        Spike(225, 150,),
        Spike(300, 250),
        Spike(375, 150),
        Spike(450, 250),
        Spike(525, 150),
        Spike(600, 250),
        Spike(675, 150)
        ]

class Map4:

    blocks = [
        Block(0, 550),
        MovingBlock(400, 525, move_range=200, speed=2),
        Block(700, 425),
        MovingBlock(400, 300, move_range=200, speed=3),
        Block(0, 200),
        MovingBlock(400, 100, move_range=200, speed=4)
    ]
