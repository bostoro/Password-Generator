import os
import base64
import re
import string
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

load_dotenv()

SALT = os.getenv('SALT').encode()
ALGORITHM = hashes.SHA256()
KEY_LENGTH = 32
ITERATIONS = 480000

def derive_key(master_password: str) -> bytes:
    kdf = PBKDF2HMAC(
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

def get_password_strength(password: str):
    has_lower = re.search(r"[a-z]", password)
    has_upper_cases = re.search(r"[A-Z]", password)
    has_digits = re.search(r"\d", password)
    has_special_characters = re.search(f"[{re.escape(string.punctuation)}]", password)
    length = len(password)
    if length < 6 or not has_lower or not has_upper_cases or not has_digits:
        return "Weak"
    if length >= 12 and has_lower and has_upper_cases and has_digits and has_special_characters:
        return "Strong"
    return "Medium"