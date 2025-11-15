import random  # For generating random passwords
import string  # Contains letters, numbers, symbols
import getpass  # For hiding password input
import datastore_reloaded as vault
import password_utils

from datastore import PasswordDataStore
from input_utils import input_boolean, input_integer, input_password, input_string_notnull

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
    answer = input_integer(f"Password length (default {length}): ", True)

    # If user entered something, use that length
    if answer:
        length = int(answer)

    # STEP 2: Ask user which character types to include
    print("\nCharacter types to include:")
    use_uppercase = input_boolean("Include UPPERCASE letters (A-Z)? (Y/n): ")
    use_lowercase = input_boolean("Include lowercase letters (a-z)? (Y/n): ")
    use_numbers = input_boolean("Include numbers (0-9)? (Y/n): ")
    use_symbols = input_boolean("Include symbols (!@#$%...)? (Y/n): ")

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
    save = input_boolean("\nDo you want to save this password? (y/N): ")

    if save:
        # Ask for information
        username = input_string_notnull("Username or email: ").strip()
        platform = input_string_notnull("Website (eg: https://facebook.com): ").strip()

        # Save in database
        store = PasswordDataStore()
        saved_id = store.save_password(username, platform, password)
        print(f"✅ Password saved with ID: {saved_id}")


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
    id_to_delete = input_integer("Enter password ID to delete: ")

    # STEP 2: Delete from database
    store = PasswordDataStore()
    deleted = store.delete_password(id_to_delete)

    # STEP 3: Show result
    if deleted:
        print(f"✅ Password with ID {id_to_delete} deleted!")
    else:
        print(f"⚠️  No password found with ID {id_to_delete}")

def update_master_password():
    updating_password = True
    while updating_password:
        old_password = input_password("Type in the old master password: ")
        if not vault.check_master_password(old_password):
            print("❌ Wrong master password!")
            updating_password = input_boolean("Would you like to retry? (Y/n): ")
            continue
        
        new_password = input_password("Type in the new master password: ")
        if vault.update_master_password(old_password, new_password):
            print("✅ Successfully updated master password!")
            updating_password = False
        else:
            print("❌ Failed to update master password!")
            updating_password = input_boolean("Would you like to retry? (Y/n): ")

def check_password_stength():
    password = input_string_notnull("Type the password to check: ")
    strength = password_utils.get_password_strength(password)

    if strength == "weak":
        print("❌ Your password is weak.")
    elif strength == "strong":
        print("🔐 Your password is strong.")
    else:
        print("✅ Your password is fine (not weak, but not strong enough).")


def show_menu():
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║         PASSWORD MANAGER - Simplified Version            ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print("\nWhat do you want to do?")
    print("  1. Generate random password")
    print("  2. Save password manually")
    print("  3. View all saved passwords")
    print("  4. Delete a password")
    print("  5. Update master password")
    print("  6. Check password stength")
    print("  7. Exit")
    print("\n💡 Master password to view passwords: 123456")

def check_master_password():
    while not vault.master_password_exists():
        print("⚠️  Before running the application, please set up the master password")
        response = getpass.getpass("\n🔒 Type in new master password: ").strip()
        if response:
            vault.set_master_password(response)
            print("✅ Master password successfully set!")

def main():
    vault.init_database()
    
    check_master_password()

    while True:
        show_menu()

        print("-" * 60)
        choice = input("Choose an option (1-6): ").strip()

        if choice == '1':
            generate_random_password()

        elif choice == '2':
            save_password_manually()

        elif choice == '3':
            show_saved_passwords()

        elif choice == '4':
            delete_password()

        elif choice == '5':
            update_master_password()

        elif choice == '6':
            check_password_stength()

        elif choice == '7':
            print("\n👋 Goodbye!")
            break

        else:
            print("⚠️  Invalid option! Choose a number from 1 to 6.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
