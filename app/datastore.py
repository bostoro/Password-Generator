import os
import sqlite3
import utils.password_utils as pe
from dotenv import load_dotenv
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import utils.password_utils as pe
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
    connection = sqlite3.connect(DB_FILE_NAME)
    cursor = connection.cursor()
    reencrypted = _reencrypt_all_passwords(cursor,
                                           old_master_password,
                                           new_master_password)
    if not reencrypted:
        connection.rollback()
        connection.close()
        return False
    encrypted_new_master = pe.encrypt_password(
        new_master_password,
        new_master_password
    )
    cursor.execute(
        'UPDATE meta SET master_password = ? WHERE id = 1',
        (encrypted_new_master,)
    )
    connection.commit()
    connection.close()
    return True


def save_password(username, platform, password, master_password):
    encrypted_password = pe.encrypt_password(password, master_password)

    connection = sqlite3.connect(DB_FILE_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute('''
            INSERT INTO passwords (username, platform, password)
            VALUES (?, ?, ?)
        ''', (username, platform, encrypted_password))
        password_id = cursor.lastrowid
        connection.commit()
        return password_id
    except sqlite3.IntegrityError:
        connection.rollback()
        return None
    finally:
        connection.close()


def get_all_passwords(master_password, show_real_passwords=False):
    connection = sqlite3.connect(DB_FILE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        'SELECT id, username, platform, password, created_at FROM passwords'
    )
    rows = cursor.fetchall()
    connection.close()

    results = []

    for row in rows:
        pwd_id = row[0]
        username = row[1]
        platform = row[2]
        encrypted_password = row[3]
        date = row[4]

        if show_real_passwords:
            password = pe.decrypt_password(encrypted_password, master_password)
        else:
            password = '********'

        results.append((pwd_id, username, platform, password, date))

    return results


def delete_password(password_id):
    connection = sqlite3.connect(DB_FILE_NAME)
    cursor = connection.cursor()

    cursor.execute('DELETE FROM passwords WHERE id = ?', (password_id,))

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted
