import os
import sqlite3
import subprocess
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests
# Configuration
API_KEY = "814254e9d1fb4859da3f4798b86b6f49"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
POSTER_FOLDER = "./posters"
DB_PATH = os.path.join(os.getcwd(), "movies.db")

# URLs for different categories
NOW_PLAYING_URL = f"https://api.themoviedb.org/3/movie/now_playing?api_key={API_KEY}&language=en-US&page=1"
TOP_RATED_URL = f"https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page=1"
UPCOMING_URL = f"https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}&language=en-US&page=1"
GENRES_URL = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"

# Create folders if they don't exist
os.makedirs(POSTER_FOLDER, exist_ok=True)

# Create database if not exists
def initialize_database():
    # if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create movies table
        cursor.execute("DROP TABLE IF EXISTS movies;")
        cursor.execute("""
        CREATE TABLE movies (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            release_date TEXT,
            overview TEXT,
            vote_average REAL,
            poster_path TEXT,
            category TEXT NOT NULL,
            genres TEXT
        );
        """)

        cursor.execute("DROP TABLE IF EXISTS user;")
        cursor.execute("""
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vorname VARCHAR(20) NOT NULL,
            nachname VARCHAR(50) NOT NULL,
            password VARCHAR(30) NOT NULL,
            email VARCHAR(30) NOT NULL UNIQUE,
            role VARCHAR(10) NOT NULL
        );
        """)

        cursor.execute("DROP TABLE IF EXISTS showtime;")
        cursor.execute("""
        CREATE TABLE showtime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date VARCHAR(50),
            time VARCHAR(50)
        );
        """)

        cursor.execute("DROP TABLE IF EXISTS reservation;")
        cursor.execute("""
        CREATE TABLE reservation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_price DECIMAL(10, 2) DEFAULT NULL,
            time_of_reservation DATETIME NOT NULL,
            user_id INT,
            showtime_id INT,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (showtime_id) REFERENCES showtime(id)
        );
        """)

        cursor.execute("DROP TABLE IF EXISTS hall;")
        cursor.execute("""
        CREATE TABLE hall (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(20) NOT NULL,
            row_count INT NOT NULL,
            seats_per_row INT NOT NULL,
            total_seats INT NOT NULL
        );
        """)

        cursor.execute("DROP TABLE IF EXISTS seat;")
        cursor.execute("""
        CREATE TABLE seat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status VARCHAR(20) NOT NULL,
            row_number INT NOT NULL,
            seat_number INT NOT NULL,
            price DECIMAL(10, 2) DEFAULT NULL,
            reservation_id INT,
            hall_id INT,
            FOREIGN KEY (reservation_id) REFERENCES reservation(id),
            FOREIGN KEY (hall_id) REFERENCES hall(id)
        );
        """)

        cursor.execute("DROP TABLE IF EXISTS showtime_includes_movie;")
        cursor.execute("""
        CREATE TABLE showtime_includes_movie (
            movie_id INT,
            showtime_id INT,
            PRIMARY KEY (movie_id, showtime_id),
            FOREIGN KEY (movie_id) REFERENCES movie(id),
            FOREIGN KEY (showtime_id) REFERENCES showtime(id)
        );
        """)

        cursor.execute("DROP TABLE IF EXISTS movie_in_hall;")
        cursor.execute("""
        CREATE TABLE movie_in_hall (
            movie_id INT,
            hall_id INT,
            PRIMARY KEY (movie_id, hall_id),
            FOREIGN KEY (movie_id) REFERENCES movie(id),
            FOREIGN KEY (hall_id) REFERENCES hall(id)
        );
        """)

        cursor.execute("DROP TABLE IF EXISTS logs_history;")
        cursor.execute("""
        CREATE TABLE logs_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action VARCHAR(100) NOT NULL,
            action_timestamp DATETIME NOT NULL,
            user_id INT,
            reservation_id INT,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (reservation_id) REFERENCES reservation(id)
        );
        """)

        conn.commit()
        conn.close()
        print("Database initialized.")

# Save movie to database
def save_movie_to_db_with_category(movie, category):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO movies (id, title, release_date, overview, vote_average, poster_path, category, genres)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        movie['id'],
        movie['title'],
        movie['release_date'],
        movie['overview'],
        movie['vote_average'],
        movie['poster_path'],
        category,
        ", ".join([genre['name'] for genre in movie['genres']]) if 'genres' in movie else None
    ))
    conn.commit()
    conn.close()

# Fetch genres from TMDB
def fetch_genres():
    response = requests.get(GENRES_URL)
    if response.status_code == 200:
        genres = response.json().get('genres', [])
        genres_dict = {genre['id']: genre['name'] for genre in genres}
        print("Fetched genres:", genres_dict)
        return genres_dict
    else:
        print("Failed to fetch genres")
        return {}

# Fetch movies from TMDB by category and save to database
def fetch_movies_by_category(category_url, category_name, genres_dict):
    response = requests.get(category_url)
    if response.status_code == 200:
        movies = response.json().get('results', [])
        for movie in movies:
            title = movie['title']
            poster_path = movie.get('poster_path')
            if poster_path:
                full_poster_url = f"{IMAGE_BASE_URL}{poster_path}"
                try:
                    image_response = requests.get(full_poster_url)
                    image_response.raise_for_status()
                    local_poster_path = os.path.join(POSTER_FOLDER, f"{title.replace(' ', '_')}.jpg")
                    image = Image.open(BytesIO(image_response.content))
                    image.save(local_poster_path)
                    movie['poster_path'] = f"/posters/{title.replace(' ', '_')}.jpg"
                except Exception as e:
                    print(f"Error downloading poster for {title}: {e}")
                    movie['poster_path'] = None
            else:
                movie['poster_path'] = None

            # Add genres to the movie
            movie['genres'] = [
                {"id": genre_id, "name": genres_dict.get(genre_id, "Unknown")}
                for genre_id in movie.get('genre_ids', [])
            ]

            save_movie_to_db_with_category(movie, category_name)
            print(f"Saved movie: {title} in category: {category_name}")
    else:
        print(f"Failed to fetch movies from {category_name}: {response.status_code}")

# Fetch and save movies for all categories
def fetch_and_save_movies():
    genres_dict = fetch_genres()

    print("Fetching Now Playing movies...")
    fetch_movies_by_category(NOW_PLAYING_URL, "now_playing", genres_dict)

    print("Fetching Top Rated movies...")
    fetch_movies_by_category(TOP_RATED_URL, "top_rated", genres_dict)

    print("Fetching Upcoming movies...")
    fetch_movies_by_category(UPCOMING_URL, "upcoming", genres_dict)

# API endpoint to get movies by category
@app.route('/api/movies/<category>', methods=['GET'])
def get_movies_by_category(category):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, release_date, overview, vote_average, poster_path, genres
        FROM movies WHERE category = ?
    """, (category,))
    movies = cursor.fetchall()
    conn.close()
    return jsonify([
        {
            "id": movie[0],
            "title": movie[1],
            "release_date": movie[2],
            "overview": movie[3],
            "vote_average": movie[4],
            "poster_path": movie[5],
            "genres": movie[6]
        }
        for movie in movies
    ])

# Serve posters
@app.route('/posters/<filename>')
def get_poster(filename):
    return send_from_directory(POSTER_FOLDER, filename)

# Start the frontend
def start_frontend():
    frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
    print(f"Frontend path: {frontend_path}")  # Debugging line
    subprocess.Popen(["npm", "start"], cwd=frontend_path)

if __name__ == "__main__":
    initialize_database()
    fetch_and_save_movies()
    start_frontend()
    app.run(debug=True)
