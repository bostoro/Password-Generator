import os
import utils.password_utils as pe
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from model.models import Base, Meta, Password

DB_FILE_NAME = os.getenv('DB_FILE_NAME')

load_dotenv()

_engine = create_engine(f"sqlite:///{DB_FILE_NAME}")


def _get_engine():
    return _engine


def init_database():
    Base.metadata.create_all(_get_engine())


def master_password_exists(username: str) -> bool:
    with Session(_get_engine()) as session:
        return session.query(Meta).filter_by(username=username).first() is not None


def set_master_password(username: str, master_password: str) -> bool:
    with Session(_get_engine()) as session:
        if session.query(Meta).filter_by(username=username).first() is not None:
            return False
        encrypted_master = pe.encrypt_password(master_password, master_password)
        session.add(Meta(username=username, master_password=encrypted_master))
        session.commit()
        return True


def check_master_password(username: str, master_password: str) -> bool:
    with Session(_get_engine()) as session:
        meta = session.query(Meta).filter_by(username=username).first()
        if meta is None:
            return False
        try:
            decrypted = pe.decrypt_password(meta.master_password, master_password)
            return decrypted == master_password
        except Exception:
            return False


def get_meta(username: str) -> Meta | None:
    with Session(_get_engine()) as session:
        return session.query(Meta).filter_by(username=username).first()


def _reencrypt_all_passwords(
        session: Session,
        meta_id: int,
        old_master_password: str,
        new_master_password: str) -> bool:
    passwords = session.query(Password).filter_by(meta_id=meta_id).all()
    for pwd in passwords:
        try:
            decrypted = pe.decrypt_password(pwd.password, old_master_password)
            pwd.password = pe.encrypt_password(decrypted, new_master_password)
        except Exception:
            return False
    return True


def update_master_password(
        username: str,
        old_master_password: str,
        new_master_password: str) -> bool:
    if not check_master_password(username, old_master_password):
        return False
    with Session(_get_engine()) as session:
        meta = session.query(Meta).filter_by(username=username).first()
        reencrypted = _reencrypt_all_passwords(session, meta.id, old_master_password, new_master_password)
        if not reencrypted:
            return False
        meta.master_password = pe.encrypt_password(new_master_password, new_master_password)
        session.commit()
        return True


def save_password(meta_id: int, username: str, platform: str, password: str, master_password: str):
    encrypted_password = pe.encrypt_password(password, master_password)
    with Session(_get_engine()) as session:
        try:
            entry = Password(meta_id=meta_id, username=username, platform=platform, password=encrypted_password)
            session.add(entry)
            session.commit()
            return entry.id
        except Exception:
            session.rollback()
            return None


def get_all_passwords(meta_id: int, master_password: str, show_real_passwords=False):
    with Session(_get_engine()) as session:
        rows = session.query(Password).filter_by(meta_id=meta_id).all()
        results = []
        for row in rows:
            if show_real_passwords:
                password = pe.decrypt_password(row.password, master_password)
            else:
                password = '********'
            results.append((row.id, row.username, row.platform, password, row.created_at))
        return results
    

def delete_password(meta_id: int, password_id: int) -> bool:
    with Session(_get_engine()) as session:
        # Añadimos la comprobación de meta_id para evitar IDOR
        entry = session.query(Password).filter_by(id=password_id, meta_id=meta_id).first()
        if entry is None:
            return False
        session.delete(entry)
        session.commit()
        return True
    

def update_password(meta_id: int, password_id: int, username: str, platform: str, password: str, master: str) -> bool:
    encrypted_password = pe.encrypt_password(password, master)
    with Session(_get_engine()) as session:
        try:
            # Añadimos la comprobación de meta_id para evitar IDOR
            entry = session.query(Password).filter_by(id=password_id, meta_id=meta_id).first()
            if entry is None:
                return False
            entry.username = username
            entry.platform = platform
            entry.password = encrypted_password
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False