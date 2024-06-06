class ScrollingManager:
    def __init__(self, screen_width, screen_height, floor_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.floor_height = floor_height
        self.offset_x = 0
        self.offset_y = 0

    def update(self, character_x, character_y):
        # 가로 스크롤링
        if character_x < self.screen_width // 2:
            self.offset_x = 0
        elif character_x > self.screen_width // 2 and character_x < self.floor_height:
            self.offset_x = character_x - self.screen_width // 2

        # 세로 스크롤링
        if character_y > self.screen_height // 2 and character_y < self.floor_height:
            self.offset_y = character_y - self.screen_height // 2

    def apply_scroll(self, rect):
        return rect.move(-self.offset_x, -self.offset_y)

    def apply_scroll_pos(self, x, y):
        return x - self.offset_x, y - self.offset_y

    def apply_scroll_rect(self, rect):
        return pygame.Rect(rect.x - self.offset_x, rect.y - self.offset_y, rect.width, rect.height)