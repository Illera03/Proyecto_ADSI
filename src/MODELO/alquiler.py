class Alquiler:
    def __init__(self, user_id, movie_id, rental_date):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rental_date = rental_date

    def __repr__(self):
        return f"Alquiler(user_id={self.user_id}, movie_id={self.movie_id}, rental_date={self.rental_date})"
       
       
    def nuevo_alquiler(user_id, movie_id, rental_date):
            return cls(user_id, movie_id, rental_date)