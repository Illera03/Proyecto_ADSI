import json

class Review:
    def __init__(self, user_id, movie_id, rating, comment):
        self.__user_id = user_id
        self.__movie_id = movie_id
        self.__rating = rating
        self.__comment = comment

    @staticmethod
    def new_review(user_id, movie_id, rating, comment):
        # Crea y devuelve una nueva instancia de la clase Review
        return Review(user_id, movie_id, rating, comment)
    
    @classmethod
    def new_review_from_bd(cls, user_id, movie_id, rating, comment):
        """Crea y devuelve una nueva instancia de la clase Review con todos los valores personalizados."""
        instance = cls(user_id, movie_id, rating, comment)
        return instance

    def get_review_info(self):
        return json.dumps({
            "Usuario": self.__user_id,
            "Pelicula": self.__movie_id,
            "Puntuacion": self.__rating,
            "Comentario": self.__comment
            })

    def update_review_info(self, new_rate, new_comment):
        self.__rating = new_rate
        self.__comment = new_comment
        return True
    
    def get_user_id(self):
        return self.__user_id
    
    def get_movie_id(self):
        return self.__movie_id
    
    def get_movie_rating(self):
        return self.__rating
    
    def get_movie_comment(self):
        return self.__comment