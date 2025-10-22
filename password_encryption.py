import os
import base64
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

load_dotenv()

SALT = os.getenv('SALT').encode()
ALGORITHM = hashes.SHA256()
KEY_LENGTH = 32
ITERATIONS = 480000

def derive_key(master_password: str) -> bytes:
    kdf = PBKDF2(
        algorithm=ALGORITHM,
        length=KEY_LENGTH,
        salt=SALT,
        iterations=ITERATIONS,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

def encrypt_password(password: str, master_password: str) -> str:
    key = derive_key(master_password)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(password.encode())
    return encrypted.decode()

def decrypt_password(encrypted_password: str, master_password: str) -> str:
    key = derive_key(master_password)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_password.encode())
    return decrypted.decode()
