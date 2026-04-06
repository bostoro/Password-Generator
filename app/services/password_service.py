import datastore
from utils.password_utils import get_password_strength


class PasswordService:

    def save(self, username: str, platform: str, password: str, master: str) -> int | None:
        if not datastore.check_master_password(master):
            return None
        return datastore.save_password(username, platform, password, master)

    def delete(self, password_id: int) -> bool:
        return datastore.delete_password(password_id)

    def get_all(self, master: str, show_real: bool = False) -> list:
        return datastore.get_all_passwords(master, show_real_passwords=show_real)

    def check_strength(self, password: str) -> str:
        return get_password_strength(password)

    def update_master(self, old_master: str, new_master: str) -> bool:
        return datastore.update_master_password(old_master, new_master)
    
    def check_master(self, master: str) -> bool:
        return datastore.check_master_password(master)