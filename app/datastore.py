import os
import utils.password_utils as pe
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from model.orm_models import Base, Meta, Password

DB_FILE_NAME = os.getenv('DB_FILE_NAME')

load_dotenv()

_engine = create_engine(f"sqlite:///{DB_FILE_NAME}")


def _get_engine():
    return _engine


def init_database():
    Base.metadata.create_all(_get_engine())


def master_password_exists() -> bool:
    with Session(_get_engine()) as session:
        return session.get(Meta, 1) is not None


def set_master_password(master_password: str) -> bool:
    with Session(_get_engine()) as session:
        if session.get(Meta, 1) is not None:
            return False
        encrypted_master = pe.encrypt_password(master_password, master_password)
        session.add(Meta(id=1, master_password=encrypted_master))
        session.commit()
        return True


def check_master_password(master_password: str) -> bool:
    with Session(_get_engine()) as session:
        meta = session.get(Meta, 1)
        if meta is None:
            return False
        try:
            decrypted = pe.decrypt_password(meta.master_password, master_password)
            return decrypted == master_password
        except Exception:
            return False


def _reencrypt_all_passwords(
        session: Session,
        old_master_password: str,
        new_master_password: str) -> bool:
    passwords = session.query(Password).all()
    for pwd in passwords:
        try:
            decrypted = pe.decrypt_password(pwd.password, old_master_password)
            pwd.password = pe.encrypt_password(decrypted, new_master_password)
        except Exception:
            return False
    return True


def update_master_password(
        old_master_password: str,
        new_master_password: str) -> bool:
    if not check_master_password(old_master_password):
        return False
    with Session(_get_engine()) as session:
        reencrypted = _reencrypt_all_passwords(session, old_master_password, new_master_password)
        if not reencrypted:
            return False
        meta = session.get(Meta, 1)
        meta.master_password = pe.encrypt_password(new_master_password, new_master_password)
        session.commit()
        return True


def save_password(username, platform, password, master_password):
    encrypted_password = pe.encrypt_password(password, master_password)
    with Session(_get_engine()) as session:
        try:
            entry = Password(username=username, platform=platform, password=encrypted_password)
            session.add(entry)
            session.commit()
            return entry.id
        except Exception:
            session.rollback()
            return None


def get_all_passwords(master_password, show_real_passwords=False):
    with Session(_get_engine()) as session:
        rows = session.query(Password).all()
        results = []
        for row in rows:
            if show_real_passwords:
                password = pe.decrypt_password(row.password, master_password)
            else:
                password = '********'
            results.append((row.id, row.username, row.platform, password, row.created_at))
        return results


def delete_password(password_id):
     with Session(_get_engine()) as session:
        entry = session.get(Password, password_id)
        if entry is None:
            return False
        session.delete(entry)
        session.commit()
        return True
