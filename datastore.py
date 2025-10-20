import os
import sqlite3
from typing import Optional
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

DB_FILE = "vault.db"
encryption_key: Optional[bytes] = None

def _assert_initialized():
    if encryption_key is None:
        raise RuntimeError("The datastore is not initialized. Call init_store(passphrase) first.")

def _derive_key(passphrase: str, salt: bytes) -> bytes:
    key_deriver = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=310_000)
    return key_deriver.derive(passphrase.encode("utf-8"))

def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS meta(
            key TEXT PRIMARY KEY,
            value BLOB NOT NULL
        );
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            platform TEXT NOT NULL,
            password_cipher BLOB NOT NULL,
            nonce BLOB NOT NULL,
            UNIQUE(username, platform)
        );
    """)

def _load_or_create_salt(conn: sqlite3.Connection) -> bytes:
    row = conn.execute("SELECT value FROM meta WHERE key='salt';").fetchone()
    if row:
        return row[0]
    salt = os.urandom(16)
    conn.execute("INSERT INTO meta(key, value) VALUES('salt', ?);", (salt,))
    return salt

def _seal_or_verify_canary(conn: sqlite3.Connection, key: bytes) -> None:
    nonce_row = conn.execute("SELECT value FROM meta WHERE key='canary_nonce';").fetchone()
    cipher_row = conn.execute("SELECT value FROM meta WHERE key='canary_cipher';").fetchone()
    if nonce_row is None and cipher_row is None:
        nonce = os.urandom(12)
        encrypted_canary = AESGCM(key).encrypt(nonce, b"vault-canary", None)
        conn.execute("INSERT INTO meta(key, value) VALUES('canary_nonce', ?);", (nonce,))
        conn.execute("INSERT INTO meta(key, value) VALUES('canary_cipher', ?);", (encrypted_canary,))
        return
    if not nonce_row or not cipher_row:
        raise RuntimeError("Vault metadata is corrupted.")
    nonce, encrypted_canary = nonce_row[0], cipher_row[0]
    try:
        decrypted_canary = AESGCM(key).decrypt(nonce, encrypted_canary, None)
    except InvalidTag:
        raise ValueError("Invalid passphrase for this vault.")
    # if decrypted_canary != b"vault-canary":
    #     raise ValueError("Invalid passphrase for this vault.")

def init_store(passphrase: str) -> None:
    global encryption_key
    with sqlite3.connect(DB_FILE) as conn:
        _ensure_schema(conn)
        salt = _load_or_create_salt(conn)
        key = _derive_key(passphrase, salt)
        _seal_or_verify_canary(conn, key)
        encryption_key = key
        conn.commit()

def insert_account(username: str, platform: str, plaintext_password: str) -> None:
    _assert_initialized()
    associated_data = f"{username}|{platform}".encode("utf-8")
    nonce = os.urandom(12)
    encrypted_password = AESGCM(encryption_key).encrypt(nonce, plaintext_password.encode("utf-8"), associated_data)
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            INSERT INTO accounts (username, platform, password_cipher, nonce)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(username, platform)
            DO UPDATE SET password_cipher = excluded.password_cipher,
                          nonce = excluded.nonce;
        """, (username, platform, encrypted_password, nonce))
        conn.commit()

def delete_account(username: str, platform: str) -> bool:
    _assert_initialized()
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute(
            "DELETE FROM accounts WHERE username = ? AND platform = ?;",
            (username, platform),
        )
        conn.commit()
        return cursor.rowcount > 0

def get_password(username: str, platform: str) -> Optional[str]:
    _assert_initialized()
    associated_data = f"{username}|{platform}".encode("utf-8")
    with sqlite3.connect(DB_FILE) as conn:
        row = conn.execute(
            "SELECT password_cipher, nonce FROM accounts WHERE username = ? AND platform = ?;",
            (username, platform),
        ).fetchone()
    if not row:
        return None
    encrypted_password, nonce = row
    try:
        decrypted_password = AESGCM(encryption_key).decrypt(nonce, encrypted_password, associated_data)
        return decrypted_password.decode("utf-8")
    except Exception:
        return None

def list_accounts() -> list[tuple[str, str]]:
    _assert_initialized()
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute(
            "SELECT username, platform FROM accounts ORDER BY username, platform;"
        ).fetchall()
    return [(username, platform) for (username, platform) in rows]

def close_store() -> None:
    global encryption_key
    encryption_key = None
