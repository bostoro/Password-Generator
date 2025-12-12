import os
import sqlite3
import password_utils as pe
from dotenv import load_dotenv


load_dotenv()

DB_NAME = os.getenv('DB_FILE_NAME')


def init_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meta (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            master_password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            platform TEXT NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    connection.commit()
    connection.close()


def master_password_exists() -> bool:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM meta WHERE id = 1')
    exists = cursor.fetchone()
    connection.close()
    return exists is not None


def set_master_password(master_password: str) -> bool:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM meta WHERE id = 1')
    exists = cursor.fetchone()
    if exists:
        connection.close()
        return False
    encrypted_master = pe.encrypt_password(master_password, master_password)
    cursor.execute(
        'INSERT INTO meta (id, master_password) VALUES (1, ?)',
        (encrypted_master,)
    )
    connection.commit()
    connection.close()
    return True


def check_master_password(master_password: str) -> bool:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('SELECT master_password FROM meta WHERE id = 1')
    result = cursor.fetchone()
    connection.close()
    if not result:
        return False
    try:
        decrypted = pe.decrypt_password(result[0], master_password)
        return decrypted == master_password
    except Exception:
        return False


def _reencrypt_all_passwords(
        cursor,
        old_master_password: str,
        new_master_password: str) -> bool:
    cursor.execute('SELECT id, password FROM passwords')
    passwords = cursor.fetchall()
    for pwd_id, encrypted_password in passwords:
        try:
            decrypted = pe.decrypt_password(
                encrypted_password,
                old_master_password
            )
            re_encrypted = pe.encrypt_password(decrypted, new_master_password)
            cursor.execute(
                'UPDATE passwords SET password = ? WHERE id = ?',
                (re_encrypted, pwd_id)
            )
        except Exception:
            return False
    return True


def update_master_password(
        old_master_password: str,
        new_master_password: str) -> bool:
    if not check_master_password(old_master_password):
        return False
    connection = sqlite3.connect(DB_NAME)
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

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO passwords (username, platform, password)
        VALUES (?, ?, ?)
    ''', (username, platform, encrypted_password))

    password_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return password_id


def get_all_passwords(master_password, show_real_passwords=False):
    connection = sqlite3.connect(DB_NAME)
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
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('DELETE FROM passwords WHERE id = ?', (password_id,))

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted
