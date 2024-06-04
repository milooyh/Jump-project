class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

def create_blocks():
    return [Block(x, y) for x, y in blocks_positions]
