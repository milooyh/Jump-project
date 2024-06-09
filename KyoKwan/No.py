import subprocess
import time
import os

file_path = 'C:\\OSSW4\\your_file.txt'
repo_path = 'C:\\OSSW4'
commit_message = 'w'
branch_name = 'kyokwan'

try:
    subprocess.run(['git', 'checkout', branch_name], cwd=repo_path, check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while checking out the branch: {e}")

while True:
    if not os.path.exists(file_path):
        open(file_path, 'w').close()

    with open(file_path, 'a') as f:
        f.write('#\n')

    try:
        subprocess.run(['git', 'pull', 'origin', branch_name], cwd=repo_path, check=True)
        subprocess.run(['git', 'add', file_path], cwd=repo_path, check=True)
        subprocess.run(['git', 'commit', '-m', commit_message], cwd=repo_path, check=True)
        subprocess.run(['git', 'push', 'origin', branch_name], cwd=repo_path, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    time.sleep(10)
