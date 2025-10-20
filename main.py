#!/usr/bin/env python3
"""
SIMPLIFIED VERSION - Password Manager
Program to manage your passwords securely.

WHAT YOU CAN DO:
1. Generate random secure passwords
2. Save passwords in database (encrypted)
3. View saved passwords (with master password)
4. Delete passwords

MASTER PASSWORD: 123456
"""

import random  # For generating random passwords
import string  # Contains letters, numbers, symbols
import getpass  # For hiding password input
from datastore import PasswordDataStore  # Our database


# ============================================
# FUNCTION 1: GENERATE RANDOM PASSWORDS
# ============================================
def generate_random_password(length=16):
    """
    Creates a random and secure password with customizable options.

    HOW IT WORKS:
    1. Asks user for password length
    2. Asks which character types to include (uppercase, lowercase, numbers, symbols)
    3. Prepares a list of all chosen characters
    4. Chooses characters randomly from the list
    5. Puts them together to create the password
    6. Asks if user wants to save it

    PARAMETERS:
    - length: default password length (default: 16)

    RETURNS:
    - Nothing (displays password and optionally saves it)

    EXAMPLE:
    >>> generate_random_password()
    Password length (default 16): 12
    Include UPPERCASE letters (A-Z)? (Y/n): y
    Include lowercase letters (a-z)? (Y/n): y
    Include numbers (0-9)? (Y/n): y
    Include symbols (!@#$%...)? (Y/n): n

    ✅ Password generated: aB3xZ9mN2pQ7
       Length: 12 characters
    """
    print("\n🔐 PASSWORD GENERATOR")
    print("=" * 50)

    # STEP 1: Ask user for length
    answer = input(f"Password length (default {length}): ").strip()

    # If user entered something, use that length
    if answer:
        length = int(answer)

    # STEP 2: Ask user which character types to include
    print("\nCharacter types to include:")
    use_uppercase = input("Include UPPERCASE letters (A-Z)? (Y/n): ").strip().lower() != 'n'
    use_lowercase = input("Include lowercase letters (a-z)? (Y/n): ").strip().lower() != 'n'
    use_numbers = input("Include numbers (0-9)? (Y/n): ").strip().lower() != 'n'
    use_symbols = input("Include symbols (!@#$%...)? (Y/n): ").strip().lower() != 'n'

    # STEP 3: Prepare character sets based on user choices
    all_characters = ''

    if use_uppercase:
        all_characters += string.ascii_uppercase  # A, B, C, ..., Z

    if use_lowercase:
        all_characters += string.ascii_lowercase  # a, b, c, ..., z

    if use_numbers:
        all_characters += string.digits  # 0, 1, 2, ..., 9

    if use_symbols:
        all_characters += string.punctuation  # !, @, #, $, %, ...

    # Check if at least one character type was selected
    if not all_characters:
        print("⚠️  Warning: No character types selected. Using all character types.")
        all_characters = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation

    # STEP 4: Generate password by choosing random characters
    password = ''  # Empty string
    for i in range(length):
        # Choose a random character and add it
        random_character = random.choice(all_characters)
        password += random_character

    # STEP 5: Show the generated password
    print(f"\n✅ Password generated: {password}")
    print(f"   Length: {len(password)} characters")

    # STEP 6: Ask if they want to save it
    save = input("\nDo you want to save this password? (y/N): ").strip().lower()

    if save == 'y':
        # Ask for information
        username = input("Username or email: ").strip()
        platform = input("Website (eg: https://facebook.com): ").strip()

        # Check they're not empty
        if username and platform:
            # Save in database
            store = PasswordDataStore()
            saved_id = store.save_password(username, platform, password)
            print(f"✅ Password saved with ID: {saved_id}")
        else:
            print("⚠️  You must enter username and website!")


# ============================================
# FUNCTION 2: SHOW ALL PASSWORDS
# ============================================
def show_saved_passwords():
    """
    Shows all passwords saved in the database.

    WHAT IT DOES:
    1. Asks for master password
    2. If correct, shows real passwords
    3. If wrong, shows only ********
    """
    print("\n📋 SAVED PASSWORDS")
    print("=" * 50)

    # Create object to access database
    store = PasswordDataStore()

    # STEP 1: Ask for master password (hidden for security)
    master_pwd = getpass.getpass("\n🔒 Enter master password: ").strip()

    # STEP 2: Check if it's correct
    if store.verify_master_password(master_pwd):
        print("✅ Master password correct!\n")
        show_real = True  # Show real passwords
    else:
        print("❌ Wrong master password! Showing only ********\n")
        show_real = False  # Show asterisks

    # STEP 3: Get all passwords from database
    passwords = store.show_all_passwords(show_real_passwords=show_real)

    # STEP 4: Check if there are passwords
    if not passwords:
        print("📭 No passwords saved yet.")
        return

    # STEP 5: Show passwords in table format
    print(f"Total passwords: {len(passwords)}\n")
    print("-" * 100)
    print(f"{'ID':<5} {'USERNAME':<30} {'WEBSITE':<35} {'PASSWORD':<20}")
    print("-" * 100)

    for pwd in passwords:
        pwd_id = pwd[0]
        username = pwd[1]
        platform = pwd[2]
        password = pwd[3]
        # Don't show date for simplicity

        # Truncate (shorten) long texts
        if len(username) > 28:
            username = username[:28] + '..'
        if len(platform) > 33:
            platform = platform[:33] + '..'
        if len(password) > 18:
            password = password[:18] + '..'

        # Print the row
        print(f"{pwd_id:<5} {username:<30} {platform:<35} {password:<20}")

    print("-" * 100)


# ============================================
# FUNCTION 3: SAVE PASSWORD MANUALLY
# ============================================
def save_password_manually():
    """
    Allows user to enter and save a password manually.

    WHAT IT DOES:
    1. Asks for username, website and password
    2. Saves everything in database (password encrypted)
    """
    print("\n💾 SAVE A NEW PASSWORD")
    print("=" * 50)

    # STEP 1: Ask for information
    username = input("Username or email: ").strip()
    platform = input("Website (eg: https://facebook.com): ").strip()
    password = input("Password: ").strip()

    # STEP 2: Check they're not empty
    if not username or not platform or not password:
        print("⚠️  All fields are required!")
        return

    # STEP 3: Save in database
    store = PasswordDataStore()
    saved_id = store.save_password(username, platform, password)

    print(f"✅ Password saved with ID: {saved_id}")


# ============================================
# FUNCTION 4: DELETE A PASSWORD
# ============================================
def delete_password():
    """
    Deletes a password from database using its ID.

    WHAT IT DOES:
    1. Asks for password ID to delete
    2. Deletes it from database
    """
    print("\n🗑️  DELETE PASSWORD")
    print("=" * 50)

    # STEP 1: Ask for ID
    try:
        id_to_delete = int(input("Enter password ID to delete: ").strip())
    except ValueError:
        print("⚠️  You must enter a number!")
        return

    # STEP 2: Delete from database
    store = PasswordDataStore()
    deleted = store.delete_password(id_to_delete)

    # STEP 3: Show result
    if deleted:
        print(f"✅ Password with ID {id_to_delete} deleted!")
    else:
        print(f"⚠️  No password found with ID {id_to_delete}")


# ============================================
# FUNCTION 5: SHOW MENU
# ============================================
def show_menu():
    """
    Shows the application's main menu.
    """
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║         PASSWORD MANAGER - Simplified Version           ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print("\nWhat do you want to do?")
    print("  1. Generate random password")
    print("  2. Save password manually")
    print("  3. View all saved passwords")
    print("  4. Delete a password")
    print("  5. Exit")
    print("\n💡 Master password to view passwords: 123456")


# ============================================
# MAIN PROGRAM
# ============================================
def main():
    """
    Main function that starts the program.

    WHAT IT DOES:
    1. Shows menu
    2. Asks what you want to do
    3. Executes chosen function
    4. Repeats until you exit
    """

    # Infinite loop (continues until you choose to exit)
    while True:
        # STEP 1: Show menu
        show_menu()

        # STEP 2: Ask what to do
        print("-" * 60)
        choice = input("Choose an option (1-5): ").strip()

        # STEP 3: Execute the right function based on choice
        if choice == '1':
            generate_random_password()

        elif choice == '2':
            save_password_manually()

        elif choice == '3':
            show_saved_passwords()

        elif choice == '4':
            delete_password()

        elif choice == '5':
            print("\n👋 Goodbye!")
            break  # Exit loop

        else:
            print("⚠️  Invalid option! Choose a number from 1 to 5.")


# ============================================
# PROGRAM STARTING POINT
# ============================================
if __name__ == '__main__':
    """
    This is the starting point.
    When you run 'python3 main.py', it starts here.
    """
    main()
