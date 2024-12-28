import sqlite3
from MODELO.movie import Movie

class MovieManager:
    dbPath="data/video_club.db"

    def __init__(self, dbPath):
        self.dbPath=dbPath

    #Este metodo para conectar con la DB
    def conect(self):
        return sqlite3.connect(self.dbPath)
    
    #Este metodo carga en el atributo peliculas (Pelicula[] peliculas en Java) todas las películas de la base de datos
    def cargarGestor(self):
        conexion=self.conect()
        cursor=conexion.cursor()
        cursor.execute("SELECT id, title, genre, releaseYear, director FROM Peliculas")
        self.peliculas=[
            Movie(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4]) for tupla in cursor.fetchall()
        ]
        conexion.close()

    #Este metodo carga del atributo peliculas todas las películas en la base de datos
    def sincroDB(self): 
        conexion = self.conect()
        cursor = conexion.cursor()

        cursor.execute("SELECT id FROM Peliculas")
        ids_en_base = {fila[0] for fila in cursor.fetchall()}
        ids_en_memoria = {pelicula.id for pelicula in self.peliculas}

        ids_a_eliminar = ids_en_base - ids_en_memoria
        for id_eliminar in ids_a_eliminar:
            cursor.execute("DELETE FROM Peliculas WHERE id = ?", (id_eliminar,))

    
        for pelicula in self.peliculas:
            if pelicula.id in ids_en_base:
                cursor.execute(
                    "UPDATE Peliculas SET title = ?, genre = ?, releaseYear = ?, director = ? WHERE id = ?",
                    (pelicula.title, pelicula.genre, pelicula.releaseYear, pelicula.director, pelicula.id)
                )
            else:
                cursor.execute(
                    "INSERT INTO Peliculas (title, genre, releaseYear, director) VALUES (?, ?, ?, ?)",
                    (pelicula.title, pelicula.genre, pelicula.releaseYear, pelicula.director)
                )

        conexion.commit()
        conexion.close()
