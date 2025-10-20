# 🔐 PASSWORD MANAGER - Beginner Version

Complete password manager with encryption and master password protection. Perfect for learning Python!

**⚠️ EDUCATIONAL PROJECT - NOT FOR REAL PASSWORDS!**

---

## 🚀 QUICK START

```bash
cd /Users/fabriziocasula/Documents/ai/fh/versione_principianti
python3 main.py
```

**Master Password:** `123456`

---

## ✨ FEATURES

### 1️⃣ Generate Random Passwords
- **Customizable length** (default: 16 characters)
- **Choose character types:**
  - ✅ Uppercase letters (A-Z)
  - ✅ Lowercase letters (a-z)
  - ✅ Numbers (0-9)
  - ✅ Symbols (!@#$%...)

### 2️⃣ Save Passwords
- Passwords stored **encrypted** in SQLite database
- Save with username/email and website
- XOR encryption (educational purpose)

### 3️⃣ View Passwords
- Requires **master password** (123456)
- Shows passwords in plain text
- Master password input is **hidden** for security

### 4️⃣ Delete Passwords
- Remove passwords by ID
- Permanent deletion

---

## 📖 FILES IN THIS FOLDER

```
versione_principianti/
├── main.py                 💻 Main program (interactive menu)
├── datastore.py           💾 Database + encryption
├── README.md              📖 This file
├── IMPORTANT_NOTES.md     ⚠️  Important security notes
└── passwords.db           🔐 Database (created automatically)
```

---

## 💻 USAGE EXAMPLES

### Example 1: Generate and Save Password

```bash
$ python3 main.py

Choose an option (1-5): 1

🔐 PASSWORD GENERATOR
Password length (default 16): 20

Character types to include:
Include UPPERCASE letters (A-Z)? (Y/n): y
Include lowercase letters (a-z)? (Y/n): y
Include numbers (0-9)? (Y/n): y
Include symbols (!@#$%...)? (Y/n): y

✅ Password generated: aB3!xZ9@mN2$pQ7&hK4%
   Length: 20 characters

Do you want to save this password? (y/N): y
Username or email: john@example.com
Website (eg: https://facebook.com): https://netflix.com
✅ Password saved with ID: 1
```

### Example 2: Save Password Manually

```bash
Choose an option (1-5): 2

💾 SAVE A NEW PASSWORD
Username or email: mary@example.com
Website (eg: https://facebook.com): https://twitter.com
Password: MySecretPass123!
✅ Password saved with ID: 2
```

### Example 3: View Saved Passwords

```bash
Choose an option (1-5): 3

📋 SAVED PASSWORDS

🔒 Enter master password: [type 123456 - hidden]
✅ Master password correct!

Total passwords: 2

--------------------------------------------------------------------
ID    USERNAME              WEBSITE                   PASSWORD
--------------------------------------------------------------------
1     john@example.com      https://netflix.com       aB3!xZ9@mN2$..
2     mary@example.com      https://twitter.com       MySecretPass123!
--------------------------------------------------------------------
```

### Example 4: Delete Password

```bash
Choose an option (1-5): 4

🗑️  DELETE PASSWORD
Enter password ID to delete: 1
✅ Password with ID 1 deleted!
```

---

## 🔒 SECURITY

### How It Works

1. **Passwords Encrypted:** Stored using XOR encryption in SQLite database
2. **Master Password:** Required to view passwords in plain text
3. **Hidden Input:** Master password is hidden while typing (using `getpass`)
4. **Database File:** `passwords.db` contains encrypted passwords

### Security Features

✅ Passwords stored encrypted (not plain text)
✅ Master password protection
✅ Hidden password input
✅ Passwords shown as `********` without master password

### ⚠️ IMPORTANT WARNING

**This is an EDUCATIONAL project!**

❌ **DO NOT use for real passwords!**

XOR encryption is **NOT SECURE** for real use. It's only for learning purposes.

✅ **For real passwords, use:**
- [Bitwarden](https://bitwarden.com/) - Free, open source
- [1Password](https://1password.com/) - Professional
- [KeePass](https://keepass.info/) - Local, free

---

## 🎓 LEARNING OBJECTIVES

This project teaches:

### Python Basics
- ✅ Functions and classes
- ✅ Loops (`for`, `while`)
- ✅ Conditions (`if`, `elif`, `else`)
- ✅ User input/output
- ✅ Error handling (`try`/`except`)

### Python Libraries
- ✅ `sqlite3` - Database operations
- ✅ `base64` - Data encoding
- ✅ `getpass` - Hidden password input
- ✅ `string` - String manipulation
- ✅ `random` - Random selection

### Programming Concepts
- ✅ Data encryption (XOR algorithm)
- ✅ Database CRUD operations
- ✅ Interactive CLI menus
- ✅ User input validation
- ✅ Password security basics

---

## 📝 CODE STRUCTURE

### `main.py` - Main Program

```
main()
├── show_menu()                     # Display menu
├── generate_random_password()      # Option 1: Generate
├── save_password_manually()        # Option 2: Save
├── show_saved_passwords()          # Option 3: View (with master password)
└── delete_password()               # Option 4: Delete
```

### `datastore.py` - Database & Encryption

```
PasswordDataStore
├── __init__()                      # Initialize database
├── _create_table()                 # Create passwords table
├── _encrypt_password()             # Encrypt using XOR
├── _decrypt_password()             # Decrypt using XOR
├── save_password()                 # Save encrypted password
├── show_all_passwords()            # Get passwords (encrypted or decrypted)
├── verify_master_password()        # Check master password
└── delete_password()               # Delete by ID
```

---

## 🧪 TESTING

### Quick Test (Automated)
```bash
python3 datastore.py
```
This runs automated tests showing:
- How encryption/decryption works
- How to save passwords
- How to retrieve passwords

### Interactive Test
```bash
python3 main.py
```
Try all menu options:
1. Generate password ✅
2. Save password manually ✅
3. View passwords (master password: 123456) ✅
4. Delete password ✅
5. Exit ✅

---

## 🔧 CUSTOMIZATION

### Change Master Password

**File:** `datastore.py` (line 26)
```python
MASTER_PASSWORD = "123456"  # ← Change to your password
```

### Change Default Password Length

**File:** `main.py` (line 23)
```python
def generate_random_password(length=16):  # ← Change 16 to your default
```

### Change Encryption Key

**File:** `datastore.py` (line 38)
```python
self.secret_key = b'my_super_secret_key_2024'  # ← Change this
```

⚠️ **Warning:** Changing the key makes existing passwords unreadable!

---

## 🐛 TROUBLESHOOTING

### Problem: "ModuleNotFoundError"
**Solution:** Use Python 3
```bash
python3 --version  # Must be 3.6 or higher
python3 main.py
```

### Problem: "Permission denied"
**Solution:** Add execute permission
```bash
chmod +x main.py
python3 main.py
```

### Problem: Master password not hidden
**Solution:** The `getpass` module should hide it automatically. If you still see it, your terminal might not support it. The password is still being captured correctly.

### Problem: Can't see old passwords after changing encryption key
**Solution:** Delete the database and start fresh
```bash
rm passwords.db
python3 main.py
```

### Problem: Password not saved
**Solution:** Make sure you enter BOTH username AND website. If either is missing, the password won't be saved.

---

## 💡 TIPS FOR BEGINNERS

1. **Read the code comments** - Every line is explained!
2. **Start with datastore.py** - Understand encryption first
3. **Then read main.py** - See how the menu works
4. **Experiment!** - Try modifying the code
5. **Use print()** - Add print statements to see what's happening

---

## 📊 PROJECT STATS

- **Lines of code:** ~500 (heavily commented)
- **Python files:** 2 (`main.py`, `datastore.py`)
- **Language:** Python 3.6+
- **Database:** SQLite
- **Encryption:** XOR (educational only)
- **Dependencies:** None (standard library only)

---

## 🎯 NEXT STEPS

After completing this project:

1. ✅ Understand how XOR encryption works
2. ✅ Learn about secure encryption (AES, bcrypt)
3. ✅ Add password strength checker
4. ✅ Add export/import features
5. ✅ Create a GUI version (tkinter)
6. ✅ Build your own project!

---

## 📚 ADDITIONAL RESOURCES

- **Python Documentation:** https://docs.python.org/3/
- **SQLite Tutorial:** https://www.sqlitetutorial.net/
- **Cryptography Basics:** https://cryptography.io/
- **Python getpass:** https://docs.python.org/3/library/getpass.html

---

## ⚠️ READ THIS!

See `IMPORTANT_NOTES.md` for:
- Why master password is hidden
- Why you see "test@email.com" in automated tests
- How to verify your data is saved correctly

---

**Made with ❤️ to learn Python**

Ready to start? Run:
```bash
python3 main.py
```
