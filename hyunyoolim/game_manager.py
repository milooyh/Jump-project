import pygame # 파이게임 라이브러리 임포트
import sys # 시스템 관련 기능 제공 모듈 임포트
from pygame.locals import USEREVENT # pygame 라이브러리에서 userevent를 임포트
import subprocess  # subprocess 모듈을 추가해야 합니다.
from setting import * # 설정 파일에서 모든 설정 가져오기
from character import Character # 캐릭터 클래스 임포트
from screen import Screen # 화면 클래스 임포트
from block import Block # 발판 클래스 임포트
from obstacle import Obstacle # 장애물 클래스 임포트
from portal import Portal # 포털 클래스 임포트
from item import * # 아이템 관련 모든 설정 가져오기

# 게임 매이저 클래스
class GameManager:
    
    def __init__(self):
        pygame.init() # 파이게임 초기화
        pygame.font.init() # 폰트 초기화

        # 화면 설정 및 윈도우 생성
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("점프 점프")

        self.clock = pygame.time.Clock() # FPS 제어를 위한 clock 객체 생성
        Screen.show_start_screen(self.screen) # 시작 화면 표시

        # 바닥의 y좌표 설정
        self.floor_y = floor_y
        print(self.floor_y)

        # 블록 장애물 포탈 생성
        self.blocks = [Block(x, y) for x, y in blocks_positions]
        print(self.blocks)
        self.obstacles = [Obstacle(x, y, obstacle_speed) for x, y, obstacle_speed in obstacles_positions]
        print(self.obstacles)
        highest_block_x = max([block.x for block in self.blocks])
        print(highest_block_x)
        highest_block_y = max([block.y for block in self.blocks])
        print(highest_block_y)
        self.portal = Portal(highest_block_x, highest_block_y - 100)
        print(self.portal)

        # 아이템 생성
        self.heart_item = HeartItem(350, 350)  # 예시 좌표로 설정
        self.speed_item = SpeedItem(600, 250)  # 예시 좌표로 설정
        self.invincibility_item = InvincibilityItem(500, 150)  # 예시 좌표로 설정
        self.items = [self.heart_item, self.speed_item, self.invincibility_item]
        
        # 캐릭터 생성
        self.character = Character(self.blocks, self.obstacles, self.portal, self.items)

        self.game_over = False # 게임 종료 변수 초기화
        self.game_clear = False # 게임 클리어 변수 초기화
    
    # 게임 재설정 함수
    def reset_game(self):
        self.character.set_initial_position()
        self.character.life = 3
        self.character.game_over = False
        self.character.current_color_index = 0
        self.obstacles = [Obstacle(x, y, obstacle_speed) for x, y, obstacle_speed in obstacles_positions]
    
    # 게임 실행 함수
    def run_game(self):
        running = True # 게임 실행 여부
        font = pygame.font.Font(None, 36) # 폰트 설정
        obstacles = [Obstacle(x, y, obstacle_speed) for x, y, obstacle_speed in obstacles_positions]

        while running:
            self.screen.fill(WHITE) # 화면 흰색으로 채움
            character_rect = pygame.Rect(self.character.x, self.character.y, self.character.width, self.character.height)

            # 이벤트 처리
            for event in pygame.event.get():
                # 이벤트 종료 시
                if event.type == pygame.QUIT:
                    running = False
                    print('게임 강제 종료')
                
                # 키가 눌렸을 때
                if event.type == pygame.KEYDOWN:
                    # 스페이스바가 눌렸을 때
                    if event.key == pygame.K_SPACE:
                        self.character.space_pressed = True
                        print('스페이스바 눌림')
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.character.space_pressed = False
                        print('스페이스바 안 눌림')

            if not self.character.game_over and not self.character.game_clear:
                self.character.update_game_state()
                print('게임 상태 업데이트')

                self.character.draw_game_elements(self.screen, self.blocks, self.obstacles, self.portal)
                print('게임 요소 그리기')
                
                # 장애물 위치 업데이트
                for obstacle in self.obstacles:
                    obstacle.update_position()
                    if obstacle.x < -obstacle_width:
                        obstacle.x = SCREEN_WIDTH
                    
                life_text = font.render(f"Life: {self.character.life}", True, BLACK)
                life_rect = life_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
                self.screen.blit(life_text, life_rect)
                
                self.heart_item.draw(self.screen)
                self.speed_item.draw(self.screen)
                self.invincibility_item.draw(self.screen)
                print('아이템 그리기')

                if self.character.game_clear:
                    print('게임 클리어')
                    # 포탈과 충돌하면 main.py 실행
                    subprocess.run(["python", "johwangyu/main.py"])
                    break
                elif self.character.game_over:
                    print('게임오버')
                    Screen.show_game_over_screen(self.screen, self)
                    
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.run_game()
