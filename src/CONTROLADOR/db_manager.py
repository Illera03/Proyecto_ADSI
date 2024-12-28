import sqlite3
from CONTROLADOR.user_management import UserManager
from CONTROLADOR.alquiler_management import AlquilerManager
from CONTROLADOR.movie_management import MovieManager
from CONTROLADOR.request_management import RequestManager

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
        """Crear una conexión a la base de datos SQLite."""
        #self.conn = sqlite3.connect(self.db_file)
        if not hasattr(self, "conn") or self.conn is None:
            self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
            self.conn.execute("PRAGMA journal_mode=WAL;")  # Habilitar modo WAL
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
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuarios")
        usuarios = cursor.fetchall()
        # Iterar por cada usuario y agregarlo al UserManager
        for usuario in usuarios:
            username = usuario[1] 
            password = usuario[2]  
            email = usuario[3]     
            role = usuario[4]     
            status = usuario[5]    
            user_manager.add_user_from_bd(username, password, email, role, status)
        
        user_manager.print_users()
        
        # Iterar por cada alquiler y agregarlo al AlquilerManager
        alquiler_manager = AlquilerManager(self.db_file)
        self.create_connection()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Alquileres")
        alquileres = cursor.fetchall()
        for alquiler in alquileres:
            user_id = alquiler[0]
            movie_id = alquiler[1]
            rental_date = alquiler[2]
            alquiler_manager.add_alquiler_from_bd(user_id, movie_id, rental_date)
        
        # Iterar por cada película y agregarla al MovieManager
        movie_manager = MovieManager()
        self.create_connection()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Películas")
        peliculas = cursor.fetchall()
        for pelicula in peliculas:
            movie_id = pelicula[0]
            title = pelicula[1]
            genre = pelicula[2]
            release_year = pelicula[3]
            director = pelicula[4]
            notaPromedio = pelicula[5]
            idAdminAceptado = pelicula[6]
            movie_manager.add_movie_from_bd(movie_id, title, genre, release_year, director, notaPromedio, idAdminAceptado)
        
        # Iterar por cada peticion y agregarla al RequestManager
        request_manager = RequestManager()
        self.create_connection()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Peticiones")
        peticiones = cursor.fetchall()
        for peticion in peticiones:
            movie_id = peticion[0]
            user_id = peticion[1]
            status = peticion[2]
            request_manager.add_request_from_bd(movie_id, user_id, status=False)

        
        # TODO Cargar datos de películas, alquileres, etc..."""

    
    def delete_user(self, username):
        """Eliminar un usuario de la base de datos."""
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Usuarios WHERE username = ?", (username,))
            conn.commit()
            print(f"Usuario {username} eliminado")
            return True
        except sqlite3.OperationalError as e:
            print(f"Error al eliminar usuario: {e}")
            return False
        finally:
            cursor.close() 

    
        
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
        finally:
            cursor.close()
            
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
    def save_rental(self, user_id, movie_id):
        """ Guardar un alquiler en la base de datos """
        self.create_connection()
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO Alquileres (user_id, movie_id) VALUES (?, ?)", (user_id, movie_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error al guardar alquiler: {e}")
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

    # Métodos para pruebas

    def exists_user(self, username):
        """Verificar si un usuario existe en la bd"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result is not None
    
    def get_user(self, username):
        """Obtener un usuario de la bd"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result