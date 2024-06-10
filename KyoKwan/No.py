import subprocess
import time
import os

file_path = 'C:\\OSSW4\\your_file.txt'  # 경로 확인
repo_path = 'C:\\OSSW4'                 # 경로 확인
commit_message = 'w'                    # 커밋 메시지
branch_name = 'kyokwan'                 # 브랜치 이름
main_branch = 'main'                    # 메인 브랜치 이름

def run_git_command(commands, repo_path):
    try:
        subprocess.run(commands, cwd=repo_path, check=True)
    except subprocess.CalledProcessError as e:
        print(f"오류: {e}")
        return False
    return True

def resolve_conflicts(repo_path):
    try:
        # 모든 변경 사항을 스테이징
        run_git_command(['git', 'add', '-A'], repo_path)
        # 병합 커밋 수행
        run_git_command(['git', 'commit', '-m', 'Resolved conflicts'], repo_path)
    except subprocess.CalledProcessError as e:
        print(f"충돌 해결 중 오류 발생: {e}")

try:
    run_git_command(['git', 'checkout', branch_name], repo_path)
except subprocess.CalledProcessError as e:
    print(f"오류: {e}")

while True:
    if not os.path.exists(file_path):
        open(file_path, 'w').close()

    with open(file_path, 'a') as f:
        f.write('#\n')

    try:
        run_git_command(['git', 'pull', 'origin', branch_name], repo_path)
        run_git_command(['git', 'add', file_path], repo_path)
        run_git_command(['git', 'commit', '-m', commit_message], repo_path)
        run_git_command(['git', 'push', 'origin', branch_name], repo_path)

        # 메인 브랜치 체크아웃
        run_git_command(['git', 'checkout', main_branch], repo_path)
        # 메인 브랜치 최신 상태로 업데이트
        run_git_command(['git', 'pull', 'origin', main_branch], repo_path)
        # 작업 브랜치를 메인 브랜치에 병합
        if not run_git_command(['git', 'merge', '--strategy-option=theirs', branch_name], repo_path):
            # 충돌 발생 시 해결 시도
            resolve_conflicts(repo_path)
        # 메인 브랜치 푸시
        run_git_command(['git', 'push', 'origin', main_branch], repo_path)
        # 다시 작업 브랜치로 돌아가기
        run_git_command(['git', 'checkout', branch_name], repo_path)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    time.sleep(30)  # 커밋 쿨타임
