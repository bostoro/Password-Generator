"""
SIMPLIFIED VERSION - Password Manager Database
This file handles saving passwords in a SQLite database.

BASIC CONCEPTS:
- SQLite Database: a file that contains a table (like Excel)
- Encryption: transform the password into secret code
- Decryption: transform the secret code back into readable password
"""

import sqlite3  # Library for working with databases
import base64   # Library for encoding data


class PasswordDataStore:
    """
    This class manages all operations with the password database.

    WHAT IT DOES:
    - Saves passwords in encrypted form
    - Retrieves passwords and decrypts them when needed
    - Checks the master password
    """

    # The MASTER PASSWORD to view saved passwords
    MASTER_PASSWORD = "123456"

    def __init__(self):
        """
        This function runs automatically when we create the object.

        WHAT IT DOES:
        1. Defines the database file name: 'passwords.db'
        2. Defines a secret key to encrypt passwords
        3. Creates the table in the database if it doesn't exist
        """
        self.db_name = 'passwords.db'  # Database file name
        self.secret_key = b'my_super_secret_key_2024'  # Key for encryption
        self._create_table()

    def _create_table(self):
        """
        Creates the 'passwords' table in the database if it doesn't exist.

        THE TABLE HAS THESE COLUMNS:
        - id: automatic number (1, 2, 3...)
        - username: username or email
        - platform: website (eg: https://facebook.com)
        - password: ENCRYPTED password
        - created_at: creation date
        """
        # STEP 1: Open connection to database
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # STEP 2: Create the table (if it doesn't exist)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                platform TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # STEP 3: Save changes and close
        connection.commit()
        connection.close()

    def _encrypt_password(self, plain_password):
        """
        Encrypts (hides) the password using XOR encryption.

        HOW XOR WORKS:
        Imagine having numbers: password = 65, key = 12
        65 XOR 12 = 77 (encrypted password)
        77 XOR 12 = 65 (original password) - works both ways!

        PARAMETERS:
        - plain_password: the normal password (eg: "MyPassword123")

        RETURNS:
        - encrypted password in base64 format (eg: "aGVsbG8=")
        """
        # STEP 1: Convert password to numbers (bytes)
        password_in_numbers = plain_password.encode('utf-8')

        # STEP 2: Prepare an empty list for encrypted numbers
        encrypted_numbers = []

        # STEP 3: For each character in the password, apply XOR
        for index, number in enumerate(password_in_numbers):
            # Get a character from the key (cyclically)
            key_char = self.secret_key[index % len(self.secret_key)]
            # Apply XOR and add to the list
            encrypted_numbers.append(number ^ key_char)

        # STEP 4: Convert encrypted numbers to base64 text
        encrypted_password = base64.b64encode(bytes(encrypted_numbers)).decode('utf-8')

        return encrypted_password

    def _decrypt_password(self, encrypted_password):
        """
        Decrypts (shows) the password using XOR encryption.

        PARAMETERS:
        - encrypted_password: password in base64 format (eg: "aGVsbG8=")

        RETURNS:
        - plain password (eg: "MyPassword123")
        """
        try:
            # STEP 1: Convert from base64 to numbers
            encrypted_numbers = base64.b64decode(encrypted_password.encode('utf-8'))

            # STEP 2: Prepare list for decrypted numbers
            decrypted_numbers = []

            # STEP 3: Apply XOR to decrypt (same process as encryption!)
            for index, number in enumerate(encrypted_numbers):
                key_char = self.secret_key[index % len(self.secret_key)]
                decrypted_numbers.append(number ^ key_char)

            # STEP 4: Convert numbers to text
            plain_password = bytes(decrypted_numbers).decode('utf-8')

            return plain_password

        except Exception as error:
            # If there's an error, return an error message
            return f"[ERROR: cannot decrypt]"

    def save_password(self, username, platform, password):
        """
        Saves a new password entry in the database (in ENCRYPTED form).

        PARAMETERS:
        - username: username or email
        - platform: website (URL)
        - password: password to save

        RETURNS:
        - id: identification number of the saved password

        EXAMPLE:
        >>> store = PasswordDataStore()
        >>> id = store.save_password("mario@email.com", "https://facebook.com", "Password123")
        >>> print(f"Password saved with ID: {id}")
        Password saved with ID: 1
        """
        # STEP 1: Encrypt the password
        encrypted_password = self._encrypt_password(password)

        # STEP 2: Open connection to database
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # STEP 3: Insert data into the table
        cursor.execute('''
            INSERT INTO passwords (username, platform, password)
            VALUES (?, ?, ?)
        ''', (username, platform, encrypted_password))

        # STEP 4: Get the ID of the just inserted row
        password_id = cursor.lastrowid

        # STEP 5: Save and close
        connection.commit()
        connection.close()

        return password_id

    def show_all_passwords(self, show_real_passwords=False):
        """
        Retrieves all passwords from the database.

        PARAMETERS:
        - show_real_passwords:
            * True = show decrypted passwords (plain text)
            * False = show ******** (hidden)

        RETURNS:
        - list of tuples: [(id, username, platform, password, date), ...]

        EXAMPLE:
        >>> store = PasswordDataStore()
        >>> passwords = store.show_all_passwords(show_real_passwords=False)
        >>> for pwd in passwords:
        ...     print(pwd)
        (1, 'mario@email.com', 'https://facebook.com', '********', '2025-10-19')
        """
        # STEP 1: Open connection to database
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # STEP 2: Select all rows from the table
        cursor.execute('SELECT id, username, platform, password, created_at FROM passwords')
        rows = cursor.fetchall()  # Get all rows

        # STEP 3: Close the connection
        connection.close()

        # STEP 4: Prepare the results list
        results = []

        for row in rows:
            pwd_id = row[0]
            username = row[1]
            platform = row[2]
            encrypted_password = row[3]
            date = row[4]

            # If we need to show real passwords, decrypt them
            if show_real_passwords:
                password = self._decrypt_password(encrypted_password)
            else:
                # Otherwise show asterisks
                password = '********'

            # Add to list
            results.append((pwd_id, username, platform, password, date))

        return results

    def verify_master_password(self, input_password):
        """
        Checks if the master password is correct.

        PARAMETERS:
        - input_password: the password the user entered

        RETURNS:
        - True if correct
        - False if wrong

        EXAMPLE:
        >>> store = PasswordDataStore()
        >>> if store.verify_master_password("123456"):
        ...     print("Access granted!")
        ... else:
        ...     print("Wrong password!")
        Access granted!
        """
        return input_password == self.MASTER_PASSWORD

    def delete_password(self, password_id):
        """
        Deletes a password from the database using its ID.

        PARAMETERS:
        - password_id: the ID number of the password to delete

        RETURNS:
        - True if deletion was successful
        - False if ID doesn't exist

        EXAMPLE:
        >>> store = PasswordDataStore()
        >>> if store.delete_password(1):
        ...     print("Password deleted!")
        ... else:
        ...     print("ID not found!")
        Password deleted!
        """
        # STEP 1: Open connection
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        # STEP 2: Delete the row with that ID
        cursor.execute('DELETE FROM passwords WHERE id = ?', (password_id,))

        # STEP 3: Check if at least one row was deleted
        deleted = cursor.rowcount > 0

        # STEP 4: Save and close
        connection.commit()
        connection.close()

        return deleted


# ========================================
# USAGE EXAMPLE (to understand how it works)
# ========================================
if __name__ == '__main__':
    """
    This code runs only if you launch this file directly.
    It's useful for testing the functions.
    """

    print("=== PASSWORD MANAGER TEST ===\n")

    # Create the object to manage the database
    store = PasswordDataStore()

    # Example 1: Save a password
    print("1. Saving a password...")
    new_id = store.save_password(
        username="test@email.com",
        platform="https://test.com",
        password="MySuperPassword123!"
    )
    print(f"   ✓ Password saved with ID: {new_id}\n")

    # Example 2: Show all passwords (hidden)
    print("2. Showing passwords (hidden)...")
    passwords = store.show_all_passwords(show_real_passwords=False)
    for pwd in passwords:
        print(f"   ID: {pwd[0]} | User: {pwd[1]} | Password: {pwd[3]}")
    print()

    # Example 3: Verify master password
    print("3. Verifying master password...")
    if store.verify_master_password("123456"):
        print("   ✓ Master password correct!\n")

        # Example 4: Show real passwords
        print("4. Showing real passwords...")
        passwords = store.show_all_passwords(show_real_passwords=True)
        for pwd in passwords:
            print(f"   ID: {pwd[0]} | User: {pwd[1]} | Password: {pwd[3]}")
    else:
        print("   ✗ Master password wrong!\n")
