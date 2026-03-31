import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import pytest
import datastore
from utils.password_utils import get_password_strength

# Fixture that runs automatically before each test.
# Creates a clean, temporary SQLite database to avoid affecting your real data.
@pytest.fixture(autouse=True)
def setup_test_db(tmp_path):
    # Overwrite the DB_NAME variable in datastore to use a temporary file
    test_db_path = tmp_path / "test_db.sqlite"
    datastore.DB_NAME = str(test_db_path)
    
    # Initialize the tables
    datastore.init_database()
    
    yield # The test runs here

# 1. Username + Website
def test_unique_username_platform_pair():
    master_pwd = "MasterPassword123!"
    datastore.set_master_password(master_pwd)
    
    # Save the first time (should be successful and return an ID)
    id_1 = datastore.save_password("bostoro", "github.com", "mi_pass_1", master_pwd)
    assert id_1 is not None, "Should be able to save the first password"
    
    # Try to save ANOTHER password with the SAME username and platform
    id_2 = datastore.save_password("bostoro", "github.com", "mi_pass_2", master_pwd)
    
    # The result must be None because it violates the UNIQUE(username, platform) constraint
    assert id_2 is None, "Should fail when saving a duplicate username+platform"

# 2. Master Password Lifecycle
def test_master_password_lifecycle():
    # It shouldn't exist at the beginning
    assert not datastore.master_password_exists()
    
    # Configured successfully
    assert datastore.set_master_password("StrongMaster!")
    assert datastore.master_password_exists()
    
    # Verify that the login works
    assert datastore.check_master_password("StrongMaster!")
    assert not datastore.check_master_password("WrongMaster!")

# 3. Save and Retrieve Passwords
def test_save_and_retrieve_passwords():
    master = "Master123!"
    datastore.set_master_password(master)
    
    # Save passwords
    datastore.save_password("user1", "siteA.com", "secret1", master)
    datastore.save_password("user2", "siteB.com", "secret2", master)
    
    # Retrieve masked (show_real_passwords=False)
    masked_results = datastore.get_all_passwords(master, show_real_passwords=False)
    assert len(masked_results) == 2
    assert masked_results[0][3] == "********", "The password should be masked"
    
    # Retrieve real passwords (show_real_passwords=True)
    real_results = datastore.get_all_passwords(master, show_real_passwords=True)
    # real_results is a list of tuples: (id, username, platform, password, date)
    assert real_results[0][3] == "secret1", "Should decrypt and show the real password"

# 4. Update Master Password (Re-encryption)
def test_update_master_password_reencrypts_data():
    old_master = "OldMaster!"
    new_master = "NewMaster123!"
    
    datastore.set_master_password(old_master)
    datastore.save_password("test_user", "test_site", "my_secret", old_master)
    
    # Update the master password
    success = datastore.update_master_password(old_master, new_master)
    assert success is True
    
    # Verify that we cannot access with the old one
    assert not datastore.check_master_password(old_master)
    assert datastore.check_master_password(new_master)
    
    # Verify that the saved password was re-encrypted and can be read with the new master password
    results = datastore.get_all_passwords(new_master, show_real_passwords=True)
    assert results[0][3] == "my_secret"

# 5. Delete Passwords
def test_delete_password():
    master = "Master123!"
    datastore.set_master_password(master)
    
    pwd_id = datastore.save_password("user1", "siteA", "pass1", master)
    
    # Confirm it was saved
    assert len(datastore.get_all_passwords(master)) == 1
    
    # Delete it
    deleted = datastore.delete_password(pwd_id)
    assert deleted is True
    
    # Confirm it no longer exists
    assert len(datastore.get_all_passwords(master)) == 0

# 6. Strength Evaluator
def test_password_strength_logic():
    assert get_password_strength("weak") == "weak"
    assert get_password_strength("12345") == "weak"
    assert get_password_strength("Medium123") == "medium"
    assert get_password_strength("SuperStrongP@ssw0rd!") == "strong"