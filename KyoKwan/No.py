from cryptography.fernet import Fernet
import subprocess
import time
import os

file_path = 'C:\\OSSW4\\your_file.txt'
repo_path = 'C:\\OSSW4'
commit_message = 'Automated commit'
branch_name = 'kyokwan'

key_path = 'C:\\OSSW4\\filekey.key'
if not os.path.exists(key_path):
    key = Fernet.generate_key()
    with open(key_path, 'wb') as key_file:
        key_file.write(key)
else:
    with open(key_path, 'rb') as key_file:
        key = key_file.read()

cipher_suite = Fernet(key)

def encrypt_file(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = cipher_suite.encrypt(file_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(file_path):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

try:
    subprocess.run(['git', 'checkout', branch_name], cwd=repo_path, check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while checking out the branch: {e}")

while True:
    if not os.path.exists(file_path):
        open(file_path, 'w').close()

    with open(file_path, 'a') as f:
        f.write('#\n')

    encrypt_file(file_path)

    try:
        subprocess.run(['git', 'pull', 'origin', branch_name], cwd=repo_path, check=True)
        subprocess.run(['git', 'add', file_path], cwd=repo_path, check=True)
        subprocess.run(['git', 'commit', '-m', commit_message], cwd=repo_path, check=True)
        subprocess.run(['git', 'push', 'origin', branch_name], cwd=repo_path, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

    decrypt_file(file_path)

    time.sleep(10)
