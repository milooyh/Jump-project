import subprocess
import time
import os

# 파일 경로 설정
file_path = 'C:\\OSSW4\\your_file.txt'

# 레포지토리 경로 설정
repo_path = 'C:\\OSSW4'

# 커밋 메시지 설정
commit_message = '#'

while True:
    # 파일이 존재하지 않으면 생성
    if not os.path.exists(file_path):
        open(file_path, 'w').close()
    
    # 파일에 # 추가
    with open(file_path, 'a') as f:
        f.write('#\n')
    
    # git 명령어 실행
    subprocess.run(['git', 'add', file_path], cwd=repo_path)
    subprocess.run(['git', 'commit', '-m', commit_message], cwd=repo_path)
    subprocess.run(['git', 'push'], cwd=repo_path)
    
    # 30초 대기
    time.sleep(30)
