import pygame
from portal import Portal

# 화면 높이를 저장할 변수 추가
SCREEN_HEIGHT = None

# 바닥 속성 설정
floor_height = 150  # 바닥 두께
floor_y = None  # SCREEN_HEIGHT 대신 직접 값을 사용하고 있으므로 변경

# 발판 속성 설정
platform_width, platform_height = 100, 20
platform_color = (0, 0, 255)

# 블록 좌표 설정
blocks_positions = [
    (100, 325),  # 왼쪽 첫 번째 발판 밑에 추가
    # (100, 500),
    # (300, 400),
    (500, 325),  # 수정: 왼쪽 두 번째 발판 위치 변경
    # (700, 200)
]

# 블록 클래스 정의
class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 블록 리스트 초기화
blocks = [Block(x, y) for x, y in blocks_positions]

# 캐릭터 사망 여부
is_dead = False

# 충돌 감지
def check_collision(character, blocks):
    for block in blocks:
        if character.colliderect(pygame.Rect(block.x, block.y, platform_width, platform_height)):
            return block
    return None

# 스테이지 1 초기화 함수
def initialize(screen_height):
    global floor_y, SCREEN_HEIGHT  # 전역 변수로 사용하기 위해 선언
    SCREEN_HEIGHT = screen_height  # 전달받은 화면 높이를 저장
    floor_y = SCREEN_HEIGHT - floor_height  # 바닥 y 좌표 설정

# 스테이지 1 그리기
def draw(screen):
    global floor_y  # 전역 변수로 사용하려면 선언 필요

    pygame.draw.rect(screen, (144, 228, 144), (0, floor_y, 800, floor_height))  # 바닥 그리기

    # 발판 그리기
    for block in blocks:
        pygame.draw.rect(screen, platform_color, (block.x, block.y, platform_width, platform_height))

    # 빨간색 가시 발판 그리기
    red_spike_x, red_spike_y = blocks_positions[0][0], floor_y - platform_height - 10  # 조그만 아래로 위치 조정
    
    # 3개의 삼각형 산 모양으로 변경
    pygame.draw.polygon(screen, (255, 0, 0), [(red_spike_x, red_spike_y),
                                              (red_spike_x + platform_width // 2, red_spike_y - platform_height),
                                              (red_spike_x + platform_width, red_spike_y)])  # 삼각형 산 모양 그리기

    red_spike_x, red_spike_y = blocks_positions[1][0], floor_y - platform_height - 10  # 조그만 아래로 위치 조정
    pygame.draw.polygon(screen, (255, 0, 0), [(red_spike_x, red_spike_y),
                                              (red_spike_x + platform_width // 2, red_spike_y - platform_height),
                                              (red_spike_x + platform_width, red_spike_y)])  # 삼각형 산 모양 그리기

    # 포탈 그리기
    portal = Portal(750, floor_y - 80)  # 화면 오른쪽 끝에 가깝게 포탈 생성
    portal.draw(screen)

    if is_dead:
        font = pygame.font.SysFont(None, 50)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (400 - text.get_width() // 2, 300 - text.get_height() // 2))

    pygame.display.flip()