from doctest import master

import datastore
from utils.password_utils import get_password_strength
import string
import secrets
class PasswordService:

    def __init__(self, username: str, meta_id: int):
        self._username = username
        self._meta_id = meta_id

    def save(self, username: str, platform: str, password: str, master: str) -> int | None:
        if not datastore.check_master_password(self._username, master):
            return None
        return datastore.save_password(self._meta_id, username, platform, password, master)

    def delete(self, password_id: int) -> bool:
        return datastore.delete_password(self._meta_id, password_id)

    def get_all(self, master: str, show_real: bool = False) -> list:
        return datastore.get_all_passwords(self._meta_id, master, show_real_passwords=show_real)

    def check_strength(self, password: str) -> str:
        return get_password_strength(password)

    def update_master(self, old_master: str, new_master: str) -> bool:
        return datastore.update_master_password(self._username, old_master, new_master)
    
    def check_master(self, master: str) -> bool:
        return datastore.check_master_password(self._username, master)
    
    def update_password(self, password_id: int, username: str, platform: str, password: str, master: str) -> bool:
        if not datastore.check_master_password(self._username, master):
            return False
        return datastore.update_password(self._meta_id, password_id, username, platform, password, master)
    
    def generate(self, length: int = 16, use_upper: bool = True, use_lower: bool = True, use_numbers: bool = True, use_symbols: bool = True) -> str:
        all_chars = ''
        if use_upper: all_chars += string.ascii_uppercase
        if use_lower: all_chars += string.ascii_lowercase
        if use_numbers: all_chars += string.digits
        if use_symbols: all_chars += string.punctuation
        if not all_chars:
            all_chars = string.ascii_letters + string.digits
        if length <= 0:
            return ''
        return ''.join(secrets.choice(all_chars) for _ in range(length))