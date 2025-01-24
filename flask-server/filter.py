import os
import sqlite3
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cinema_functions_for_database import get_movie_runtime, get_movie_genre, get_movie_adult, get_movie, get_movie_id

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Gehe ein Verzeichnis nach oben
DB_PATH = os.path.join(BASE_DIR, 'cinema.db')

def filter_movies_by_duration(min_duration, max_duration):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    query = "SELECT id FROM movie"
    cur.execute(query)
    movie_ids = cur.fetchall()

    filtered_movies = []
    for movie_id in movie_ids:
        runtime = get_movie_runtime(movie_id[0])
        if runtime is not None and min_duration <= runtime <= max_duration:
            movie = get_movie(movie_id[0])
            filtered_movies.append(movie)

    con.close()
    return filtered_movies

def filter_movies_by_genre(selected_genre):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    query = "SELECT id FROM movie"
    cur.execute(query)
    movie_ids = cur.fetchall()

    filtered_movies = []
    for movie_id in movie_ids:
        genre = get_movie_genre(movie_id[0])
        if genre is not None and selected_genre.lower() == genre.lower():
            movie = get_movie(movie_id[0])
            filtered_movies.append(movie)

    con.close()
    return filtered_movies

def filter_movies_by_age(age_rating):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    query = "SELECT id FROM movie"
    cur.execute(query)
    movie_ids = cur.fetchall()

    filtered_movies = []
    for movie_id in movie_ids:
        adult_rating = get_movie_adult(movie_id[0])

        if adult_rating is None:
            continue

        if age_rating == 'PG' and adult_rating == 0:
            movie = get_movie(movie_id[0])
            filtered_movies.append(movie)
        elif age_rating == 'R' and adult_rating == 1:
            movie = get_movie(movie_id[0])
            filtered_movies.append(movie)

    con.close()
    return filtered_movies