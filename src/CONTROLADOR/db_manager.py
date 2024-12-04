import sqlite3

def create_connection(db_file):
    """ Crear una conexión a la base de datos SQLite """
    conn = sqlite3.connect(db_file)
    return conn

def create_tables(conn):
    """ Crear las tablas necesarias en la base de datos """
    cursor = conn.cursor()


    #cursor.execute(''' DROP TABLE IF EXISTS Reseñas; ''')
    #cursor.execute(''' DROP TABLE IF EXISTS Alquileres; ''')
    #cursor.execute(''' DROP TABLE IF EXISTS Películas; ''')
    #cursor.execute(''' DROP TABLE IF EXISTS Usuarios; ''')
    #cursor.execute(''' DROP TABLE IF EXISTS Peticiones; ''')

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
   
    # Tabla Películas
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

    # Tabla Alquileres
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS "Alquileres" (
        user_id	INTEGER,
        movie_id INTEGER,
        rental_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY("user_id","movie_id","rental_date"),
        FOREIGN KEY("movie_id") REFERENCES "Películas"("movie_id"),
        FOREIGN KEY("user_id") REFERENCES "Usuarios"("user_id")
);
    ''')
    
    # Tabla Reseñas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reseñas (
        user_id	INTEGER,
        movie_id INTEGER,
        rating REAL,
        comment TEXT,
        PRIMARY KEY("user_id","movie_id"),
        FOREIGN KEY("movie_id") REFERENCES "Películas"("movie_id"),
        FOREIGN KEY("user_id") REFERENCES "Usuarios"("user_id")
);
    ''')
    
    # Tabla Peticiones
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Peticiones (
        movie_id INTEGER,
        user_id INTEGER,
        status TEXT DEFAULT 'pendiente',
        PRIMARY KEY("user_id","movie_id"),
        FOREIGN KEY("movie_id") REFERENCES "Películas"("movie_id"),
        FOREIGN KEY("user_id") REFERENCES "Usuarios"("user_id")
);
    ''')
        
    cursor.execute('''
                   INSERT INTO Películas (title, genre,release_year, director, notaPromedio,idAdminAceptado) VALUES
                   ("El señor de los anillos","Accion",2001,"Peter Jackson", 0,1),
                   ("Gladiator","Accion",2000,"Ridley Scott", 0,2),
                   ("Harry Potter","Accion",2001,"Chris Columbus", 0,3),
                   ("Titanic","Romance",1997,"James Cameron", 0,4),
                   ("El Padrino","Drama",1972,"Francis Ford Coppola", 0,3),
                   ("El Rey León","Animación",1994,"Roger Allers", 0,4),
                   ("La lista de Schindler","Drama",1993,"Steven Spielberg", 0,1),
                   ("El club de la lucha","Drama",1999,"David Fincher", 0,2),
                   ("El sexto sentido","Drama",1999,"M. Night Shyamalan", 0,1),
                   ("El silencio de los corderos","Drama",1991,"Jonathan Demme", 0,2),
                   ("El resplandor","Terror",1980,"Stanley Kubrick", 0,3),
                   ("Origen","Ciencia Ficción",2010,"Christopher Nolan", 0,4),
                   ("Batman: El caballero de la noche","Accion",2008,"Christopher Nolan", 0,1);
                   ''')
    conn.commit()

