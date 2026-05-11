# Password Manager – Browser App

**Problem**
Memorizing and generating new passwords can be annoying. Users tend to repeat rather than randomize. Also, there is no feedback on whether the password is good or bad. This is why users need a safe, local way to create and manage passwords. The tool should list available commands, let users customize password generation, keep records with usernames and platforms, and provide strength feedback — all without relying on external services.

**Scenario**
The application allows users to:
- register and log in with a master password
- generate strong, customizable passwords
- save passwords linked to a username and platform
- view, edit, and delete saved passwords
- reveal individual passwords on demand
- update their master password

**User stories:**
### 1. Register / Login
**As a user, I want to register or log in with a master password in order to access my password vault.**

- **Inputs:** username (`str`), master password (`str`)
- **Outputs:** access to password vault

---

### 2. Generate Password
**As a user, I want to generate a secure random password with custom options in order to get a strong password without thinking of one myself.**

- **Inputs:** length (`int`), use uppercase (`bool`), use lowercase (`bool`), use numbers (`bool`), use symbols (`bool`)
- **Outputs:** generated password (`str`), strength indicator

---

### 3. Save Password
**As a user, I want to save a password linked to a username and platform in order to keep track of my credentials.**

- **Inputs:** username (`str`), platform (`str`), password (`str`)
- **Outputs:** confirmation of saved entry

---

### 4. View Passwords
**As a user, I want to see all my saved passwords after login in order to manage them.**

- **Inputs:** none
- **Outputs:** list of entries with username, platform, masked password, date

---

### 5. Reveal Password
**As a user, I want to reveal a single password on demand in order to see it without exposing all passwords at once.**

- **Inputs:** password ID (`int`)
- **Outputs:** decrypted password shown in the table

---

### 6. Edit Password
**As a user, I want to edit a saved entry in order to keep my credentials up to date.**

- **Inputs:** password ID (`int`), updated username (`str`), platform (`str`), password (`str`)
- **Outputs:** updated entry in the table

---

### 7. Delete Password
**As a user, I want to delete a saved entry in order to remove credentials I no longer need.**

- **Inputs:** password ID (`int`)
- **Outputs:** entry removed from the table

---

### 8. Update Master Password
**As a user, I want to update my master password in order to keep my vault secure.**

- **Inputs:** old master password (`str`), new master password (`str`)
- **Outputs:** confirmation, all passwords re-encrypted

---

## 🧩 Use Cases

### Main Use Cases
- Register / Login (User)
- Generate Password (User)
- Save Password (User)
- View Passwords (User)
- Reveal Password (User)
- Edit Password (User)
- Delete Password (User)
- Update Master Password (User)
- Copy Password to Clipboard (User)

### Actors
- User

---

---

## 🏛️ Architecture

### Layers
- **UI (Presentation Layer):** NiceGUI browser-based interface. The browser acts as a thin client — no business logic or persistent state lives here.
- **Application Logic (Server-Side):** Python classes handle all business logic. UI components are instantiated as Python objects on the server.
- **Persistence Layer:** SQLite database accessed via SQLAlchemy ORM — no raw SQL statements.

### Design Patterns Used

- **Strategy Pattern:** Used in password generation. Each character set (uppercase, lowercase, numbers, symbols) is its own strategy class in `utils/password_strategies.py`. The generator composes them at runtime based on user selection.

- **Singleton Pattern:** The `PasswordService` instance is created once at login and reused across the entire session via a global registry in `layout.py`.

### Design Decisions

- Master password is stored in `PasswordService` at login and used internally — UI never passes it around after authentication.
- All passwords are encrypted at rest using the master password as the encryption key. Decryption only happens on demand when the user clicks the eye icon.
- User isolation is enforced at the database level — every query filters by `meta_id` to prevent one user accessing another's data.



---

## ✅ Project Requirements

### 1. Browser-based App (NiceGUI)

The application runs in the browser via NiceGUI. Users can register, log in, generate, save, view, edit, delete, and reveal passwords — all from the browser.

---

### 2. Data Validation

- Username and platform are required when saving a password
- Password length must be at least 1 when generating
- Master password is verified on login, registration, and master password update
- Duplicate username + platform combinations are rejected

---

### 3. Database Management (ORM)

All data is managed via SQLAlchemy. No raw SQL is used. Entities: `Meta` (user + master password), `Password` (encrypted credentials).

---

## 📂 Repository Structure

```text
Password-Generator/
├── app/
│   ├── main.py
│   ├── datastore.py
│   ├── test_datastore.py
│   ├── model/
│   │   └── models.py
│   ├── services/
│   │   └── password_service.py
│   ├── ui/
│   │   ├── layout.py
│   │   ├── view_passwords.py
│   │   ├── save_password.py
│   │   ├── generate_password.py
│   │   ├── update_master.py
│   │   └── exit_app.py
│   └── utils/
│       ├── password_utils.py
│       └── password_strategies.py
├── .env
├── requirements.txt
└── README.md
```
---

## ⚙️ How to Run

### 1. Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root:
```
DB_FILE_NAME=vault.db
SALT="password_generator_salt_2024"
STYLES_PATH="styles.json"
```

### 3. Launch
```bash
python3 app/main.py
```
Open the URL printed in the console.

### 4. Usage
1. Register with a username and master password
2. Log in to access your vault
3. Use `+` to add a new password
4. Click the eye icon to reveal a password
5. Use the edit or delete icons to manage entries
6. Click the key icon in the header to update your master password

---

## 🧪 Testing

```bash
cd app
pytest test_datastore.py -v
```

### Test Coverage
- Unique username + platform pair enforcement
- Master password lifecycle (set, check, wrong password)
- Save and retrieve passwords (masked and real)
- Master password update re-encrypts all passwords
- Delete password
- Password strength logic
- Update password
- Duplicate update rejection
- User isolation (users cannot access each other's data)---

## 👥 Team & Contributions

| Name          | Contribution                                         |
|---------------|------------------------------------------------------|
| Andrii Vlasov | Data storage, encryption, ORM, database layer        |
| Aaron Casula  | UI design, view logic, table interactions            |
| José Gédance  | Password generation, service layer, architecture     |
| Jorge Mena    | Testing, architecture, database layer                |


## 📝 License

This project is provided for **educational use only** as part of the Programming Foundations module.  
[MIT License](LICENSE)