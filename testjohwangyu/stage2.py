from portal import Portal

class Stage2:
    def __init__(self):
        self.blocks_positions = [
            (100, 550),
            (300, 450),
            (500, 350),
            (700, 250)
        ]
        self.portal = Portal(SCREEN_WIDTH - 50, SCREEN_HEIGHT - 150)