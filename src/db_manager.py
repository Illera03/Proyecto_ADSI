import sqlite3

def create_connection(db_file):
    """ Crear una conexión a la base de datos SQLite """
    conn = sqlite3.connect(db_file)
    return conn

def create_tables(conn):
    """ Crear las tablas necesarias en la base de datos """
    cursor = conn.cursor()
    
    # Tabla Usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        role TEXT NOT NULL DEFAULT 'user'
    );
    ''')
    
    # Tabla Películas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Películas (
        movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        genre TEXT,
        release_year INTEGER,
        director TEXT,
        available_copies INTEGER DEFAULT 0
    );
    ''')

    # Tabla Alquileres
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Alquileres (
        rental_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        movie_id INTEGER,
        rental_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        return_date DATETIME,
        FOREIGN KEY (user_id) REFERENCES Usuarios (user_id),
        FOREIGN KEY (movie_id) REFERENCES Películas (movie_id)
    );
    ''')
    
    # Tabla Reseñas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reseñas (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        movie_id INTEGER,
        rating INTEGER,
        comment TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Usuarios (user_id),
        FOREIGN KEY (movie_id) REFERENCES Películas (movie_id)
    );
    ''')
    
    # Tabla Peticiones
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Peticiones (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        movie_title TEXT NOT NULL,
        request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'pendiente',
        FOREIGN KEY (user_id) REFERENCES Usuarios (user_id)
    );
    ''')

    cursor.execute('''
                   DELETE FROM Películas;
                      ''')
    
    cursor.execute('''
                   INSERT INTO Películas (title, genre,release_year, director,available_copies) VALUES
                   ("Harry","Accion",2012,"sfgdf", 5),
                   ("Harry2","Accion",2012,"sfgdf", 5),
                   ("Harry3","Accion",2012,"sfgdf", 5),
                   ("Harry4","Accion",2012,"sfgdf", 5);
                   ''')
    conn.commit()

