import random  # For generating random passwords
import string  # Contains letters, numbers, symbols
import datastore
import password_utils
from input_utils import input_boolean, input_integer
from input_utils import input_password, input_string_notnull


def generate_random_password(length=16):

    print("\n🔐 PASSWORD GENERATOR")
    print("=" * 50)

    answer = input_integer(f"Password length (default {length}): ", True)

    if answer is not None:
        length = answer
    if length <= 0:
        print("⚠️  Error: Password length must be greater than 0!")
        return

    print("\nCharacter types to include:")
    use_uppercase = input_boolean("Include UPPERCASE letters (A-Z)? (y/n): ")
    use_lowercase = input_boolean("Include lowercase letters (a-z)? (y/n): ")
    use_numbers = input_boolean("Include numbers (0-9)? (y/n): ")
    use_symbols = input_boolean("Include symbols (!@#$%...)? (y/n): ")

    all_characters = ''

    if use_uppercase:
        all_characters += string.ascii_uppercase  # A, B, C, ..., Z

    if use_lowercase:
        all_characters += string.ascii_lowercase  # a, b, c, ..., z

    if use_numbers:
        all_characters += string.digits  # 0, 1, 2, ..., 9

    if use_symbols:
        all_characters += string.punctuation  # !, @, #, $, %, ...

    if not all_characters:
        print("⚠️  Warning: No character types selected. Using all types.")
        all_characters = (
            string.ascii_uppercase +
            string.ascii_lowercase +
            string.digits +
            string.punctuation
        )

    password = ''  # Empty string
    for i in range(length):
        random_character = random.choice(all_characters)
        password += random_character

    print(f"\n✅ Password generated: {password}")
    print(f"   Length: {len(password)} characters")

    save = input_boolean("\nDo you want to save this password? (y/n): ")

    if save:
        master_password = None
        while not master_password:
            response = input_password("\n🔒 Enter master password: ")
            if response.strip().lower() in ("q", "quit"):
                return
            elif datastore.check_master_password(response):
                master_password = response
            else:
                print("❌ Wrong master password! Type Q to quit.")

        username = input_string_notnull("Username or email: ").strip()
        platform = input_string_notnull(
            "Website (eg: https://facebook.com): "
        ).strip()

        saved_id = datastore.save_password(
            username,
            platform,
            password,
            master_password
        )
        print(f"✅ Password saved with ID: {saved_id}")


def show_saved_passwords():
    print("\n📋 SAVED PASSWORDS")
    print("=" * 50)

    master_pwd = input_password("\n🔒 Enter master password: ")

    if datastore.check_master_password(master_pwd):
        print("✅ Master password correct!\n")
        show_real = True
    else:
        print("❌ Wrong master password! Showing only ********\n")
        show_real = False

    passwords = datastore.get_all_passwords(master_pwd, show_real)

    if not passwords:
        print("📭 No passwords saved yet.")
        return

    print(f"Total passwords: {len(passwords)}\n")
    print("-" * 100)
    print(f"{'ID':<5} {'USERNAME':<30} {'WEBSITE':<35} {'PASSWORD':<20}")
    print("-" * 100)

    for pwd in passwords:
        pwd_id = pwd[0]
        username = pwd[1]
        platform = pwd[2]
        password = pwd[3]

        # Truncate (shorten) long texts for it to look compact
        if len(username) > 28:
            username = username[:28] + '..'
        if len(platform) > 33:
            platform = platform[:33] + '..'
        if len(password) > 18:
            password = password[:18] + '..'

        print(f"{pwd_id:<5} {username:<30} {platform:<35} {password:<20}")

    print("-" * 100)


def save_password_manually():
    print("\n💾 SAVE A NEW PASSWORD")
    print("=" * 50)

    master_password = None
    while not master_password:
        response = input_password("\n🔒 Enter master password: ")
        if response.lower() in ("q", "quit"):
            return
        elif datastore.check_master_password(response):
            master_password = response
        else:
            print("❌ Wrong master password! Type Q to quit.")

    username = input("Username or email: ").strip()
    platform = input("Website (eg: https://facebook.com): ").strip()
    password = input_password("Password: ")

    if not username or not platform or not password:
        print("⚠️  All fields are required!")
        return

    saved_id = datastore.save_password(
        username,
        platform,
        password,
        master_password
    )

    print(f"✅ Password saved with ID: {saved_id}")


def delete_password():
    print("\n🗑️  DELETE PASSWORD")
    print("=" * 50)

    id_to_delete = input_integer("Enter password ID to delete: ")

    deleted = datastore.delete_password(id_to_delete)

    if deleted:
        print(f"✅ Password with ID {id_to_delete} deleted!")
    else:
        print(f"⚠️  No password found with ID {id_to_delete}")


def update_master_password():
    updating_password = True
    while updating_password:
        old_password = input_password(
            "Type in the old master password: "
        )
        if not datastore.check_master_password(old_password):
            print("❌ Wrong master password!")
            updating_password = input_boolean(
                "Would you like to retry? (y/n): "
            )
            continue

        new_password = input_password("Type in the new master password: ")
        if datastore.update_master_password(old_password, new_password):
            print("✅ Successfully updated master password!")
            updating_password = False
        else:
            print("❌ Failed to update master password!")
            updating_password = input_boolean(
                "Would you like to retry? (y/n): "
            )


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


def check_master_password():
    while not datastore.master_password_exists():
        print(
            "⚠️  Before running the application, "
            "please set up the master password."
        )
        response = input_password("\n🔒 Type in new master password: ")
        datastore.set_master_password(response)
        print("✅ Master password successfully set!")


def main():
    datastore.init_database()

    check_master_password()

    while True:
        show_menu()

        print("-" * 60)
        choice = input("Choose an option (1-7): ").strip()

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
            print("⚠️  Invalid option! Choose a number from 1 to 7.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
