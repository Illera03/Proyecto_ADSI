import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.CONTROLADOR.general_management import GeneralManager



### PRUEBAS DE GESTIÓN DE USUARIOS --JORGE ILLERA RIVERA --
def test_register_user():
    # Arrange
    general_manager = GeneralManager()
    username = "test_user"
    password = "test_password"
    email = "test_email"
    # Act
    result = general_manager.register_user(username, password, email)
    # Assert
    assert result == True
    
def test_register_user_fail():
    # Arrange
    general_manager = GeneralManager()
    username = "test_user"
    password = "test_password"
    email = "test_email"
    # Act
    result = general_manager.register_user(username, password, email)
    # Assert
    assert result == False  # Cambia esto según el comportamiento esperado
    
def test_authenticate_user():
    # Arrange
    general_manager = GeneralManager()
    username = "test_user"
    password = "test_password"
    # Act
    result = general_manager.authenticate_user(username, password)
    # Assert
    assert result == True
    
def test_authenticate_user_fail():
    # Arrange
    general_manager = GeneralManager()
    username = "test_user"
    password = "test_password"
    # Act
    result = general_manager.authenticate_user(username, password)
    # Assert
    assert result == False

def test_get_user_info():
    # Arrange
    general_manager = GeneralManager()
    # Act
    result = general_manager.get_user_info()
    # Assert
    assert result == None

def test_get_all_users():
    # Arrange
    general_manager = GeneralManager()
    # Act
    result = general_manager.get_all_users()
    # Assert
    assert result == []

def test_update_user_info():
    # Arrange
    general_manager = GeneralManager()
    new_username = "test_user"
    new_email = "test_email"
    new_password = "test_password"
    # Act
    result = general_manager.update_user_info(new_username, new_email, new_password)
    # Assert
    assert result == True

def test_update_user_info_fail():
    # Arrange
    general_manager = GeneralManager()
    new_username = "test_user"
    new_email = "test_email"
    new_password = "test_password"
    # Act
    result = general_manager.update_user_info(new_username, new_email, new_password)
    # Assert
    assert result == False

def test_admin_get_user_info():
    # Arrange
    general_manager = GeneralManager()
    username = "test_user"
    # Act
    result = general_manager.admin_get_user_info(username)
    # Assert
    assert result == None

def test_delete_user():
    # Arrange
    general_manager = GeneralManager()
    username = "test_user"
    # Act
    result = general_manager.delete_user(username)
    # Assert
    assert result == True

def test_admin_update_user_info():
    # Arrange
    general_manager = GeneralManager()
    old_username = "test_user"
    new_username = "test_user"
    new_email = "test_email"
    new_password = "test_password"
    # Act
    result = general_manager.admin_update_user_info(old_username, new_username, new_email, new_password)
    # Assert
    assert result == True

def test_admin_update_user_info_fail():
    # Arrange
    general_manager = GeneralManager()
    old_username = "test_user"
    new_username = "test_user"
    new_email = "test_email"
    new_password = "test_password"
    # Act
    result = general_manager.admin_update_user_info(old_username, new_username, new_email, new_password)
    # Assert
    assert result == False

def test_admin_get_user_info():
    # Arrange
    general_manager = GeneralManager()
    username = "test_user"
    # Act
    result = general_manager.admin_get_user_info(username)
    # Assert
    assert result == None
    
def test_admin_get_user_info_fail():
    # Arrange
    general_manager = GeneralManager()
    username = "test_user"
    # Act
    result = general_manager.admin_get_user_info(username)
    # Assert
    assert result == None

def test_delete_user():
    # Arrange
    general_manager = GeneralManager()
    username = "test_user"
    # Act
    result = general_manager.delete_user(username)
    # Assert
    assert result == True

def test_delete_user_fail():
    # Arrange
    general_manager = GeneralManager()
    username = "test_user"
    # Act
    result = general_manager.delete_user(username)
    # Assert
    assert result == False

def test_admin_update_user_info():
    # Arrange
    general_manager = GeneralManager()
    old_username = "test_user"
    new_username = "test_user"
    new_email = "test_email"
    new_password = "test_password"
    # Act
    result = general_manager.admin_update_user_info(old_username, new_username, new_email, new_password)
    # Assert
    assert result == True

def test_admin_update_user_info_fail():
    # Arrange
    general_manager = GeneralManager()
    old_username = "test_user"
    new_username = "test_user"
    new_email = "test_email"
    new_password = "test_password"
    # Act
    result = general_manager.admin_update_user_info(old_username, new_username, new_email, new_password)
    # Assert
    assert result == False
