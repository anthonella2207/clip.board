from flask import Flask, request, jsonify, Blueprint
from filter import filter_movies_by_genre, filter_movies_by_duration, filter_movies_by_age
import sqlite3

filter_bp = Blueprint('filters', __name__)

@filter_bp.route('/', methods=['GET'])
def filter_movies():
    genre = request.args.get('genre')
    min_duration = request.args.get('min_duration', type=int)
    max_duration = request.args.get('max_duration', type=int)
    age_rating = request.args.get('age_rating')

    # Starte mit allen Filmen
    filtered_movies = set()

    if genre:
        filtered_movies = set(filter_movies_by_genre(genre))
    if min_duration and max_duration:
        duration_filtered = set(filter_movies_by_duration(min_duration, max_duration))
        filtered_movies = filtered_movies & duration_filtered if filtered_movies else duration_filtered
    if age_rating:
        age_filtered = set(filter_movies_by_age(age_rating))
        filtered_movies = filtered_movies & age_filtered if filtered_movies else age_filtered

    # Konvertiere das Set zurück in eine Liste
    filtered_movies = list(filtered_movies)

    return jsonify({'movies': filtered_movies})

@filter_bp.route('/available-genres', methods=['GET'])
def get_genres():
    con = sqlite3.connect("cinema.db")  # Der Pfad zur Datenbank
    cur = con.cursor()
    try:
        cur.execute("SELECT DISTINCT genre FROM movie")  # Hole alle Genres
        genres = cur.fetchall()
        genre_list = [genre[0] for genre in genres if genre[0]]  # Liste der Genres erstellen
        return jsonify({"genres": genre_list})  # Genres als JSON zurückgeben
    except Exception as e:
        print(f"Fehler beim Abrufen der Genres: {e}")
        return jsonify({"error": "Fehler beim Abrufen der Genres"}), 500
    finally:
        con.close()

