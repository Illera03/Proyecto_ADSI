
### IMPORTANTE ###
# NECESARIO INSTALAR pytest: pip install pytest
# Para ejecutar las pruebas: pytest src/test_gestion_de_usuarios.py
# Por tanto debe estar en la carpeta src para que funcione correctamente.

from CONTROLADOR.general_management import GeneralManager
from CONTROLADOR.db_manager import DbManager
from CONTROLADOR.user_management import UserManager

import json


# Usuario no registrado se registra --> Se registra el usuario correctamente

def test_register_user(): #FUNCIONA
    # Arrange
    username = "test_user"
    password = "test_password"
    email = "test_email"
    
    general_manager = GeneralManager()
    # Por si el usuario ya está registrado previamente
    db_manager = DbManager()
    user_manager = UserManager()
    db_manager.delete_user(username)
    user_manager.empty_user_list()
    
    # Act
    result = general_manager.register_user(username, password, email)
    
    # Assert
    assert result == True
    
    if result:
        # Comprobar que el usuario se ha registrado en la base de datos
        user = db_manager.exists_user(username)
        assert user == True
        
        # Comprobar que el usuario se ha registrado en el user_manager
        exist = user_manager.exists_user(username)
        assert exist == True
    
    db_manager.delete_user(username)
    user_manager.delete_user(username)
    
# Usuario previamente registrado, intenta registrarse con el mismo nombre de usuario --> No le permite registrarse ya que el nombre de usuario está en uso.

def test_register_user_already_registered(): #FUNCIONA
    # Arrange
    username = "test_user"
    password = "test_password"
    email = "test_email"
    
    general_manager = GeneralManager()
    # Por si el usuario ya está registrado previamente
    db_manager = DbManager()
    user_manager = UserManager()
    db_manager.delete_user(username)
    user_manager.empty_user_list()
    

    # Act
    result1 = general_manager.register_user(username, password, email)
    result2 = general_manager.register_user(username, password, email)
    
    # Assert
    assert result1 == True
    assert result2 == False

    if result1:
        # Comprobar que el usuario se ha registrado en la base de datos
        user = db_manager.exists_user(username)
        assert user == True
        
        # Comprobar que el usuario se ha registrado en el user_manager
        exist = user_manager.exists_user(username)
        assert exist == True

    db_manager.delete_user(username)
    user_manager.delete_user(username)
    

# Iniciar sesión no habiéndose registrado previamente --> No le permite iniciar sesión.

def test_login_user_not_registered(): #FUNCIONA
    # Arrange
    username = "userNotRegistered"
    password = "passwordFromUserNotRegistered"
    
    general_manager = GeneralManager()
    # Por si el usuario ya está registrado previamente
    db_manager = DbManager()
    user_manager = UserManager()
    db_manager.delete_user(username)
    user_manager.empty_user_list()
    
    # Act
    result = general_manager.authenticate_user(username, password)
    
    # Assert
    assert result == 2 # 2: Usuario no encontrado o credenciales incorrectas

# Iniciar sesión habiéndose registrado anteriormente --> Si un administrador ha aceptado la solicitud de registro, le permite iniciar sesión, si no no.

def test_login_user_registered(): #FUNCIONA
    # Arrange
    username = "test_user"
    password = "test_password"
    email = "test_email"
    
    general_manager = GeneralManager()
    # Por si el usuario ya está registrado previamente
    db_manager = DbManager()
    user_manager = UserManager()
    db_manager.delete_user(username)
    user_manager.empty_user_list()
    
    general_manager.register_user(username, password, email)
    
    # USUARIO SIN ACEPTAR LA SOLICITUD DE REGISTRO
    # Act
    notYetAccepted = general_manager.authenticate_user(username, password)
    
    # Assert
    assert notYetAccepted == 3 # 3: Usuario pendiente de aprobación
    
    # USUARIO ACEPTADO
    # Act
    general_manager.accept_user(username) 
    accepted = general_manager.authenticate_user(username, password)
    
    # Assert
    assert accepted == 0 # 0: Usuario autenticado
    
    # EXTRA: USUARIO RECHAZADO
    # Act
    general_manager.reject_user(username)
    rejected = general_manager.authenticate_user(username, password)
    
    # Assert
    assert rejected == 4 # 4: Usuario rechazado
    
    db_manager.delete_user(username)
    user_manager.empty_user_list()
    
    
# Un usuario actualiza sus datos personales --> Si cambia el nombre de usuario  y este no está en uso por otro usuario, le permitirá modificar sus datos.

def test_update_user_info(): #FUNCIONA
    # Arrange
    username = "test_user"
    password = "test_password"
    email = "test_email"
    
    new_username = "new_test_user"
    new_email = "new_test_email"
    
    general_manager = GeneralManager()
    # Por si los usuarios ya están registrados previamente
    db_manager = DbManager()
    user_manager = UserManager()
    db_manager.delete_user(username)
    db_manager.delete_user("test_user1")
    db_manager.delete_user(new_username)
    user_manager.empty_user_list()
    
    general_manager.register_user(username, password, email)
    general_manager.authenticate_user(username, password)
    
    # NUEVO NOMBRE DE USUARIO NO EN USO
    # Act
    result = general_manager.update_user_info(new_username, new_email)
    
    # Assert
    assert result == True
    
    if result:
        # Comprobar que el usuario se ha registrado en la base de datos y no existe el anterior
        user = db_manager.exists_user(new_username)
        assert user == True
        
        user = db_manager.exists_user(username)
        assert user == False
        
        # Comprobar que el usuario se ha registrado en el user_manager y no existe el anterior
        exist = user_manager.exists_user(new_username)
        assert exist == True
        
        exist = user_manager.exists_user(username)
        assert exist == False
    
    # NUEVO NOMBRE DE USUARIO EN USO
    # Arrange
    username1 = "test_user1"
    password1 = "test_password"
    email1 = "test_email"
    
    general_manager.register_user(username1, password1, email1)
        
    # Act
    result = general_manager.update_user_info(username1, email)
    
    # Assert
    assert result == False
    
    
    db_manager.delete_user(username1)
    db_manager.delete_user(new_username)
    user_manager.empty_user_list()
    

# Un administrador trata de eliminar una cuenta --> Se elimina la cuenta del usuario.

def test_delete_user(): #FUNCIONA
    # Arrange
    username = "test_user"
    password = "test_password"
    email = "test_email"
    
    general_manager = GeneralManager()
    # Por si el usuario ya está registrado previamente
    db_manager = DbManager()
    user_manager = UserManager()
    db_manager.delete_user(username)
    user_manager.empty_user_list()
    
    general_manager.register_user(username, password, email)
    
    # Act
    result = general_manager.delete_user(username)
    
    # Assert
    assert result == True
    
    if result:
        # Comprobar que el usuario se ha eliminado de la base de datos
        user = db_manager.exists_user(username)
        assert user == False
        
        # Comprobar que el usuario se ha eliminado del user_manager
        exist = user_manager.exists_user(username)
        assert exist == False
    
    db_manager.delete_user(username)
    user_manager.empty_user_list()
    

# Un administrador acepta una solicitud de registro --> Se acepta al usuario. Así permitiendo al usuario iniciar sesión.

def test_accept_user(): #FUNCIONA
    # Arrange
    username = "test_user"
    password = "test_password"
    email = "test_email"
    
    general_manager = GeneralManager()
    # Por si el usuario ya está registrado previamente
    db_manager = DbManager()
    user_manager = UserManager()
    db_manager.delete_user(username)
    user_manager.empty_user_list()
    
    general_manager.register_user(username, password, email)
    
    # Act
    general_manager.accept_user(username)
    result = general_manager.authenticate_user(username, password)
    
    # Assert
    assert result == 0 # 0: Usuario autenticado
    
    db_manager.delete_user(username)
    user_manager.delete_user(username)

# Un administrador modifica los datos de un usuario --> Si cambia el nombre de usuario y este no está en uso por otro usuario, le permitirá modificar los datos.

def test_admin_update_user_info(): #FUNCIONA
    # Arrange
    username = "test_user"
    password = "test_password"
    email = "test_email"
    
    new_username = "new_test_user"
    new_email = "new_test_email"
    
    general_manager = GeneralManager()
    # Por si los usuarios ya están registrados previamente
    db_manager = DbManager()
    user_manager = UserManager()
    db_manager.delete_user(username)
    db_manager.delete_user("test_user1")
    db_manager.delete_user(new_username)
    user_manager.empty_user_list()
    
    general_manager.register_user(username, password, email)
    
    # NUEVO NOMBRE DE USUARIO NO EN USO
    # Act
    result = general_manager.admin_update_user_info(username, new_username, new_email)
    
    # Assert
    assert result == True
    
    if result:
        # Comprobar que el usuario se ha registrado en la base de datos y no existe el anterior
        user = db_manager.exists_user(new_username)
        assert user == True
        
        user = db_manager.exists_user(username)
        assert user == False
        
        # Comprobar que el usuario se ha registrado en el user_manager y no existe el anterior
        exist = user_manager.exists_user(new_username)
        assert exist == True
        
        exist = user_manager.exists_user(username)
        assert exist == False
    
    # NUEVO NOMBRE DE USUARIO EN USO
    # Arrange
    old_username = new_username
    username1 = "test_user1"
    password1 = "test_password"
    email1 = "test_email"
    
    general_manager.register_user(username1, password1, email1)
        
    # Act
    result = general_manager.admin_update_user_info(old_username, username1, email)
    
    # Assert
    assert result == False
    
    user_manager.empty_user_list()
    db_manager.delete_user(username1)
    db_manager.delete_user(new_username)
    
    
    
# Un administrador rechaza la solicitud de registro de un usuario --> Desaparece la solicitud y el usuario no queda registrado (no puede inciar sesión).

def test_reject_user(): #FUNCIONA
# Arrange
    username = "test_user"
    password = "test_password"
    email = "test_email"
    
    general_manager = GeneralManager()
    # Por si el usuario ya está registrado previamente
    db_manager = DbManager()
    user_manager = UserManager()
    db_manager.delete_user(username)
    user_manager.empty_user_list()
    
    general_manager.register_user(username, password, email)
    user_manager.change_current_user("_admin_")
    
    # Act
    general_manager.reject_user(username)
    result = general_manager.authenticate_user(username, password)
    
    # Assert
    assert result == 4 # 4: Usuario rechazado
    
    db_manager.delete_user(username)
    user_manager.empty_user_list()
    
# Una persona se registra para crear un administrador, poniéndose de nombre de usuario _admin_ --> Se registra al nuevo con rol de administrador.

def test_register_admin(): #FUNCIONA
    # Arrange
    username = "_admin_"
    password = "test"
    email = "test_email"
    
    general_manager = GeneralManager()
    # Por si el usuario ya está registrado previamente
    db_manager = DbManager()
    user_manager = UserManager()
    db_manager.delete_user(username)
    user_manager.empty_user_list()
    
    # Act
    result1 = general_manager.register_user(username, password, email)
    result2 = general_manager.authenticate_user(username, password) # Deja iniciar sesión sin ser aceptado
    
    # Assert
    assert result1 == True
    assert result2 == 1 # 1: Usuario autenticado como administrador
    
    if result1:
        # Comprobar que el admin se ha registrado en la base de datos
        user = db_manager.exists_user(username)
        assert user == True
        
        # Comprobar que el admin se ha registrado en el user_manager
        exist = user_manager.exists_user(username)
        assert exist == True
        
        info_json = user_manager.get_user(username)
        info = json.loads(info_json)
        assert info["role"] == "admin" # Comprobar que el rol es de administrador
        assert info["status"] == "aceptado"
    
    
# def test_video():
#     db_manager = DbManager()
#     db_manager.delete_user("_admin_")
#     db_manager.delete_user("usuario1")
#     db_manager.delete_user("usuario2")
#     db_manager.delete_user("usuario3")
    
#     assert db_manager.exists_user("_admin_") == False
#     assert db_manager.exists_user("usuario1") == False
#     assert db_manager.exists_user("usuario2") == False
#     assert db_manager.exists_user("usuario3") == False
    
    
    
