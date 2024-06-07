import pygame

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        
def init_stage(stage_number):
    spikes_data = []

    if stage_number == 1:
        spikes_data = [(500, 600, 50, 20)]  # 스테이지 1에서의 가시 돌 좌표 리스트
    elif stage_number == 2:
        spikes_data = [(100, 300, 50, 20)]  # 스테이지 2에서의 가시 돌 좌표 리스트
    elif stage_number == 3:
        spikes_data = [(400, 300, 50, 20), (600, 450, 50, 20)]  # 스테이지 3에서의 가시 돌 좌표 리스트

    # 가시 돌 객체들을 생성하여 리스트에 추가
    spikes = []
    for spike_data in spikes_data:
        spikes.append(Spike(*spike_data))

    return spikes

def main():
    stages = [1, 2, 3]
    current_stage = 0

    # 스테이지 초기화
    spikes = init_stage(stages[current_stage])

    # 스테이지 시작
    for spike in spikes:
        print(spike.rect)

if __name__ == "__main__":
    main()