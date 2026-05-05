import datastore
from utils.password_utils import get_password_strength
import string
import secrets

class PasswordService:

    def __init__(self, username: str, meta_id: int, master: str):
        self._username = username
        self._meta_id = meta_id
        self._master = master

    def save(self, username: str, platform: str, password: str) -> int | None:
        return datastore.save_password(self._meta_id, username, platform, password, self._master)

    def delete(self, password_id: int) -> bool:
        return datastore.delete_password(self._meta_id, password_id)

    def get_all(self, show_real: bool = False) -> list:
        return datastore.get_all_passwords(self._meta_id, self._master, show_real_passwords=show_real)

    def get_password(self, password_id: int) -> str | None:
        return datastore.get_password_by_id(password_id, self._meta_id, self._master)

    def check_strength(self, password: str) -> str:
        return get_password_strength(password)

    def update_master(self, old_master: str, new_master: str) -> bool:
        return datastore.update_master_password(self._username, old_master, new_master)

    def check_master(self, master: str) -> bool:
        return datastore.check_master_password(self._username, master)

    def update_password(self, password_id: int, username: str, platform: str, password: str) -> bool:
        return datastore.update_password(self._meta_id, password_id, username, platform, password, self._master)

    def generate(self, length: int = 16, use_upper: bool = True, use_lower: bool = True, use_numbers: bool = True, use_symbols: bool = True) -> str:
        from utils.password_strategies import UppercaseStrategy, LowercaseStrategy, NumberStrategy, SymbolStrategy
        strategies = []
        if use_upper: strategies.append(UppercaseStrategy())
        if use_lower: strategies.append(LowercaseStrategy())
        if use_numbers: strategies.append(NumberStrategy())
        if use_symbols: strategies.append(SymbolStrategy())
        all_chars = ''.join(s.get_chars() for s in strategies)
        if not all_chars:
            all_chars = string.ascii_letters + string.digits
        if length <= 0:
            return ''
        return ''.join(secrets.choice(all_chars) for _ in range(length))