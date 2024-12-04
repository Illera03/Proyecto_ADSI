class Movie:
    def __init__(self, id, title, genre, release_year, director, nota_promedio=0.0, id_admin_aceptado=None):
        self.id = id
        self.title = title
        self.genre = genre
        self.release_year = release_year
        self.director = director
        self.nota_promedio = nota_promedio
        self.id_admin_aceptado = id_admin_aceptado
    
    def movie_with_title(self, title):
        return self.title == title
    
    def update_movie_details(self, title=None, genre=None, release_year=None, director=None):
        if title:
            self.title = title
        if genre:
            self.genre = genre
        if release_year:
            self.release_year = release_year
        if director:
            self.director = director
        return True