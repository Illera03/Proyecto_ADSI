import sqlite3
from CONTROLADOR.user_management import UserManager

class DbManager:
    _instance = None

    def __new__(cls, db_file="data/video_club.db", *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, db_file="data/video_club.db"):
        if not self.__initialized:
            self.__initialized = True
            self.db_file = db_file
            self.conn = self.create_connection()

    def create_connection(self):
        """ Crear una conexión a la base de datos SQLite """
  
        self.conn = sqlite3.connect(self.db_file)
        return self.conn

    def insert_user(self, username, password, email):
        
        self.create_connection()
        cursor = self.conn.cursor()
        role = "admin" if username.lower() == "_admin_" else "user"
        try:
            if role == "admin":
                cursor.execute(
                    "INSERT INTO Usuarios (username, password, email, role, status) VALUES (?, ?, ?, ?, 'aceptado')",
                    (username, password, email, role),
                )
            else:
                cursor.execute(
                    "INSERT INTO Usuarios (username, password, email, role, status) VALUES (?, ?, ?, ?, 'pendiente')",
                    (username, password, email, role),
                )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error al insertar usuario: {e}")
            return False
        
    def cargar_datos_iniciales(self):
        """ Pasar datos de la base de datos a la aplicación """
        """Usuarios"""
        user_manager = UserManager()
        self.create_connection()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Usuarios")
        usuarios = cursor.fetchall()
        # Iterar por cada usuario y agregarlo al UserManager
        for usuario in usuarios:
            username = usuario[1] 
            password = usuario[2]  
            email = usuario[3]     
            role = usuario[4]     
            status = usuario[5]    
            idAdmin = usuario[6]   
            user_manager.add_user_from_bd(username, password, email, role, status, idAdmin)
        
        # TODO Cargar datos de películas, alquileres, etc..."""
        user_manager.print_users()
    
    def delete_user(self, username):
        """ Eliminar un usuario de la base de datos """
        self.create_connection()
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM Usuarios WHERE username = ?", (username,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error al eliminar usuario: {e}")
            return False
        
    def update_user(self, oldUsername, newUsername, email, password=None):
        """ Actualizar la información de un usuario en la base de datos """
        self.create_connection()
        cursor = self.conn.cursor()
        try:
            if password:
                cursor.execute("UPDATE Usuarios SET username = ?, email = ?, password = ? WHERE username = ?", (newUsername, email, password, oldUsername))
            else:
                cursor.execute("UPDATE Usuarios SET username = ?, email = ? WHERE username = ?", (newUsername, email, oldUsername))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error al actualizar usuario: {e}")
            
    def save_admin(self, admin_username, username):
        """ Guardar el id del admin que aceptó o rechazó al usuario con el username dado en el usuario correspondiente """
        self.create_connection()
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT user_id FROM Usuarios WHERE username = ?", (admin_username,))
            admin_id = cursor.fetchone()[0]
            cursor.execute("UPDATE Usuarios SET idAdmin = ? WHERE username = ?", (admin_id, username))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error al guardar admin que aceptó usuario: {e}")
            return False
        
    def accept_user(self, username):
        """ Cambiar el estado de un usuario a 'aceptado' """
        self.create_connection()
        cursor = self.conn.cursor()
        try:
            cursor.execute("UPDATE Usuarios SET status = 'aceptado' WHERE username = ?", (username,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error al aceptar usuario: {e}")
            return False
    
    def reject_user(self, username):
        """ Cambiar el estado de un usuario a 'rechazado' """
        self.create_connection()
        cursor = self.conn.cursor()
        try:
            cursor.execute("UPDATE Usuarios SET status = 'rechazado' WHERE username = ?", (username,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error al rechazar usuario: {e}")
            return False

    def create_tables(self):
        """ Crear las tablas necesarias en la base de datos """
        cursor = self.conn.cursor()
        # Crear las tablas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                status TEXT DEFAULT 'Rechazado',
                idAdmin INTEGER,
                FOREIGN KEY("idAdmin") REFERENCES "Usuarios"("user_id")
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Películas (
                movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT,
                release_year INTEGER,
                director TEXT,
                notaPromedio REAL DEFAULT 0.0,
                idAdminAceptado INTEGER,
                FOREIGN KEY("idAdminAceptado") REFERENCES "Usuarios"("user_id")
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Alquileres (
                user_id INTEGER,
                movie_id INTEGER,
                rental_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY("user_id", "movie_id", "rental_date"),
                FOREIGN KEY("movie_id") REFERENCES "Películas"("movie_id"),
                FOREIGN KEY("user_id") REFERENCES "Usuarios"("user_id")
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Reseñas (
                user_id INTEGER,
                movie_id INTEGER,
                rating REAL,
                comment TEXT,
                PRIMARY KEY("user_id", "movie_id"),
                FOREIGN KEY("movie_id") REFERENCES "Películas"("movie_id"),
                FOREIGN KEY("user_id") REFERENCES "Usuarios"("user_id")
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Peticiones (
                movie_id INTEGER,
                user_id INTEGER,
                status TEXT DEFAULT 'pendiente',
                PRIMARY KEY("user_id", "movie_id"),
                FOREIGN KEY("movie_id") REFERENCES "Películas"("movie_id"),
                FOREIGN KEY("user_id") REFERENCES "Usuarios"("user_id")
            );
        ''')

        # Insertar datos iniciales
        cursor.execute('''
            INSERT INTO Películas (title, genre, release_year, director, notaPromedio, idAdminAceptado) VALUES
            ("El señor de los anillos", "Accion", 2001, "Peter Jackson", 0, 1),
            ("Gladiator", "Accion", 2000, "Ridley Scott", 0, 2),
            ("Harry Potter", "Accion", 2001, "Chris Columbus", 0, 3),
            ("Titanic", "Romance", 1997, "James Cameron", 0, 4),
            ("El Padrino", "Drama", 1972, "Francis Ford Coppola", 0, 3),
            ("El Rey León", "Animación", 1994, "Roger Allers", 0, 4),
            ("La lista de Schindler", "Drama", 1993, "Steven Spielberg", 0, 1),
            ("El club de la lucha", "Drama", 1999, "David Fincher", 0, 2),
            ("El sexto sentido", "Drama", 1999, "M. Night Shyamalan", 0, 1),
            ("El silencio de los corderos", "Drama", 1991, "Jonathan Demme", 0, 2),
            ("El resplandor", "Terror", 1980, "Stanley Kubrick", 0, 3),
            ("Origen", "Ciencia Ficción", 2010, "Christopher Nolan", 0, 4),
            ("Batman: El caballero de la noche", "Accion", 2008, "Christopher Nolan", 0, 1);
        ''')
        self.conn.commit()


