from block import Block, MovingBlock

blocks = [  
    Block(100, 500),
    Block(300, 400),
    Block(500, 300),
    Block(700, 200)
    ]

blocks = [
    Block(50, 100),
    Block(250, 400),
    Block(500, 300),
    Block(600, 200)
    ]

# 블록 좌표 설정
blocks_positions = [
    (0, 300),
    (100, 300),
    (200, 300),
    (300, 300),
    (400, 300),
    (500, 300),
    (600, 300),
    (700, 300)
]

blocks = [
    Block(0, 550),
    MovingBlock(400, 525, move_range=200, speed=2),
    Block(700, 425),
    MovingBlock(400, 300, move_range=200, speed=3),
    Block(0, 200),
    MovingBlock(400, 100, move_range=200, speed=4)
]
