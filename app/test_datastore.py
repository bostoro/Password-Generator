import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import pytest
from sqlalchemy import create_engine
import datastore
from utils.password_utils import get_password_strength

# Fixture that runs automatically before each test.
# Creates a clean, in-memory SQLite database to avoid affecting real data.
@pytest.fixture(autouse=True)
def setup_test_db(tmp_path):
    test_db_path = tmp_path / "test_db.sqlite"
    test_engine = create_engine(f"sqlite:///{test_db_path}")
    datastore._engine = test_engine

    datastore.init_database()

    yield  # The test runs here

    test_engine.dispose()

def test_unique_username_platform_pair():
    master_pwd = "MasterPassword123!"
    datastore.set_master_password("testuser", master_pwd)
    meta = datastore.get_meta("testuser")
    
    id_1 = datastore.save_password(meta.id, "bostoro", "github.com", "mi_pass_1", master_pwd)
    assert id_1 is not None, "Should be able to save the first password"
    
    id_2 = datastore.save_password(meta.id, "bostoro", "github.com", "mi_pass_2", master_pwd)
    
    assert id_2 is None, "Should fail when saving a duplicate username+platform"

def test_master_password_lifecycle():
    assert not datastore.master_password_exists("testuser")
    
    assert datastore.set_master_password("testuser", "StrongMaster!")
    assert datastore.master_password_exists("testuser")
    
    assert datastore.check_master_password("testuser", "StrongMaster!")
    assert not datastore.check_master_password("testuser", "WrongMaster!")

def test_save_and_retrieve_passwords():
    master = "Master123!"
    datastore.set_master_password("testuser", master)
    meta = datastore.get_meta("testuser")
    
    datastore.save_password(meta.id, "user1", "siteA.com", "secret1", master)
    datastore.save_password(meta.id, "user2", "siteB.com", "secret2", master)
    
    masked_results = datastore.get_all_passwords(meta.id, master, show_real_passwords=False)
    assert len(masked_results) == 2
    assert masked_results[0][3] == "********", "The password should be masked"
    
    real_results = datastore.get_all_passwords(meta.id, master, show_real_passwords=True)
    assert real_results[0][3] == "secret1", "Should decrypt and show the real password"

def test_update_master_password_reencrypts_data():
    old_master = "OldMaster!"
    new_master = "NewMaster123!"
    
    datastore.set_master_password("testuser", old_master)
    meta = datastore.get_meta("testuser")
    datastore.save_password(meta.id, "test_user", "test_site", "my_secret", old_master)
    
    success = datastore.update_master_password("testuser", old_master, new_master)
    assert success is True
    
    assert not datastore.check_master_password("testuser", old_master)
    assert datastore.check_master_password("testuser", new_master)
    
    results = datastore.get_all_passwords(meta.id, new_master, show_real_passwords=True)
    assert results[0][3] == "my_secret"

def test_delete_password():
    master = "Master123!"
    datastore.set_master_password("testuser", master)
    meta = datastore.get_meta("testuser")
    
    pwd_id = datastore.save_password(meta.id, "user1", "siteA", "pass1", master)
    
    assert len(datastore.get_all_passwords(meta.id, master)) == 1
    
    # ¡AQUÍ ESTÁ EL CAMBIO! Pasamos meta.id como primer parámetro
    deleted = datastore.delete_password(meta.id, pwd_id)
    
    assert deleted is True
    assert len(datastore.get_all_passwords(meta.id, master)) == 0

def test_password_strength_logic():
    assert get_password_strength("weak") == "weak"
    assert get_password_strength("12345") == "weak"
    assert get_password_strength("Medium123") == "medium"
    assert get_password_strength("SuperStrongP@ssw0rd!") == "strong"

def test_update_password():
    master = "Master123!"
    datastore.set_master_password("testuser", master)
    meta = datastore.get_meta("testuser")
    
    pwd_id = datastore.save_password(meta.id, "user1", "siteA", "pass1", master)
    
    success = datastore.update_password(meta.id, pwd_id, "user1_edited", "siteA_edited", "pass1_edited", master)
    
    assert success is True

def test_update_password_duplicate():
    master = "Master123!"
    datastore.set_master_password("testuser", master)
    meta = datastore.get_meta("testuser")
    
    datastore.save_password(meta.id, "user1", "siteA", "pass1", master)
    pwd_id = datastore.save_password(meta.id, "user2", "siteB", "pass2", master)
    
    success = datastore.update_password(meta.id, pwd_id, "user1", "siteA", "pass2_edited", master)
    
    assert success is False
    
def test_user_isolation():
    master_a = "MasterA123!"
    master_b = "MasterB123!"
    
    datastore.set_master_password("userA", master_a)
    datastore.set_master_password("userB", master_b)
    
    meta_a = datastore.get_meta("userA")
    meta_b = datastore.get_meta("userB")
    
    datastore.save_password(meta_a.id, "userA_account", "siteA.com", "secretA", master_a)
    datastore.save_password(meta_b.id, "userB_account", "siteB.com", "secretB", master_b)
    
    results_a = datastore.get_all_passwords(meta_a.id, master_a, show_real_passwords=True)
    results_b = datastore.get_all_passwords(meta_b.id, master_b, show_real_passwords=True)
    
    assert len(results_a) == 1
    assert len(results_b) == 1
    assert results_a[0][3] == "secretA"
    assert results_b[0][3] == "secretB"
    assert results_a[0][1] != results_b[0][1], "Users should not see each other's entries"