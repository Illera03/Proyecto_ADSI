class Request:
    def __init__(self,movie, user):
        self.movie=movie
        self.user=user
        self.estado=False

    def new_request(movie, user, status):
        return Request(movie, user, status)
    