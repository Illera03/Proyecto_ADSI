class Movie:

    def __init__(self, id, title, genre, release_year, director, nota_promedio=0.0, id_admin_aceptado=None, status=False):
        self.id = id
        self.title = title
        self.genre = genre
        self.release_year = release_year
        self.director = director
        self.nota_promedio = nota_promedio
        self.id_admin_aceptado = id_admin_aceptado
        self.status=status
    
    def movie_with_title(self, title):
        return self.title == title
    
    @staticmethod
    def new_movie(id, title, genre, release_year, director, nota_promedio=0.0, id_admin_aceptado=None, status=False):
        return Movie(id, title, genre, release_year, director, nota_promedio, id_admin_aceptado, status)
    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_genre(self):
        return self.genre

    def get_release_year(self):
        return self.release_year

    def get_director(self):
        return self.director

    def get_nota_promedio(self):
        return self.nota_promedio

    def get_id_admin_aceptado(self):
        return self.id_admin_aceptado