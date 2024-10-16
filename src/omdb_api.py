import requests

class OMDBManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://www.omdbapi.com/"

    def search_movie(self, title):
        params = {
            'apikey': self.api_key,
            't': title
        }
        response = requests.get(self.base_url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None

# Ejemplo de uso
if __name__ == "__main__":
    omdb = OMDBManager("2d79f0e")
    movie = omdb.search_movie("Harry Potter")
    
    if movie and movie['Response'] == 'True':
        print(f"Título: {movie['Title']}")
        print(f"Año: {movie['Year']}")
        print(f"Director: {movie['Director']}")
        print(f"Género: {movie['Genre']}")
    else:
        print("No se encontró la película.")
