from dotenv import load_dotenv
import os
import requests


load_dotenv(".env")
api_key = os.getenv("API_KEY")


def serialize_data(data):
    movie_data = {
        'title': data['Title'],
        'release_year': data['Year'],
        'genre': data['Genre'],
        'director': data['Director'],
        'rating': data['imdbRating'],
        'poster_url': data['Poster'],
        'plot': data['Plot']
    }
    return movie_data


def fetch_movie_info(title):
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
    res = requests.get(url)
    data = res.json()
    return serialize_data(data)




