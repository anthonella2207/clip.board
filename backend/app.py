import os
import sqlite3
import subprocess
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_cors import cross_origin
import requests
from PIL import Image
import random
from io import BytesIO
from cinema_functions_for_database import *
from routes import *
from cinema_functions_for_database import get_movie

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
app.register_blueprint(auth_routes, url_prefix="/")
app.register_blueprint(seats_routes, url_prefix="/")
app.register_blueprint(movies_routes, url_prefix="/")

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

@app.route('/routes', methods=['GET'])
def list_routes():
    from flask import jsonify
    routes = [str(rule) for rule in app.url_map.iter_rules()]
    return jsonify(routes)

# Create database if not exists
def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create movies table
    cursor.execute("DROP TABLE IF EXISTS movies;")
    cursor.execute("""
    CREATE TABLE movies (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        release_date VARCHAR(50) NOT NULL,
        overview VARCHAR(500) NOT NULL,
        vote_average REAL NOT NULL,
        poster_path VARCHAR(100) NOT NULL,
        category VARCHAR(100) NOT NULL,
        genres VARCHAR(100) NOT NULL,
        runtime INTEGER,
        adult BOOLEAN
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

    cursor.execute("DROP TABLE IF EXISTS reservation;")
    cursor.execute("""
    CREATE TABLE reservation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_price DECIMAL(10, 2) DEFAULT NULL,
        time_of_reservation DATETIME NOT NULL,
        user_id INTEGER,
        show_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES user(id),
        FOREIGN KEY (show_id) REFERENCES shows(id)
    );
    """)

    cursor.execute("DROP TABLE IF EXISTS hall;")
    cursor.execute("""
    CREATE TABLE hall (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(20) NOT NULL,
        row_count INTEGER NOT NULL,
        seats_per_row INTEGER NOT NULL,
        total_seats INTEGER NOT NULL
    );
    """)

    cursor.execute("DROP TABLE IF EXISTS seat;")
    cursor.execute("""
    CREATE TABLE seat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status VARCHAR(20) NOT NULL,
        row_number INTEGER NOT NULL,
        seat_number INTEGER NOT NULL,
        price DECIMAL(10, 2) DEFAULT NULL,
        reservation_id INTEGER,
        show_id INTEGER,
        FOREIGN KEY (reservation_id) REFERENCES reservation(id),
        FOREIGN KEY (show_id) REFERENCES shows(id)
    );
    """)

    cursor.execute("DROP TABLE IF EXISTS shows;")
    cursor.execute("""
    CREATE TABLE shows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER NOT NULL,
        hall_id INTEGER NOT NULL,
        showtime VARCHAR(50) NOT NULL,
        FOREIGN KEY (movie_id) REFERENCES movies(id),
        FOREIGN KEY (hall_id) REFERENCES hall(id)
    );
    """)

    cursor.execute("DROP TABLE IF EXISTS logs_history;")
    cursor.execute("""
    CREATE TABLE logs_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action VARCHAR(100) NOT NULL,
        action_timestamp DATETIME NOT NULL,
        user_id INTEGER,
        reservation_id INTEGER,
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
        INSERT OR IGNORE INTO movies (id, title, release_date, overview, vote_average, poster_path, category, genres, runtime, adult)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        movie['id'],
        movie['title'],
        movie['release_date'],
        movie['overview'],
        movie['vote_average'],
        movie['poster_path'],
        category,
        ", ".join([genre['name'] for genre in movie['genres']]) if 'genres' in movie else None,
        movie.get('runtime'),
        movie.get('adult', False)
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

# Fetch movie details (including runtime and adult flag)
def fetch_movie_details(movie_id):
    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(details_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch details for movie ID {movie_id}: {response.status_code}")
        return {}

# Fetch movies from TMDB by category and save to database
def fetch_movies_by_category(category_url, category_name, genres_dict):
    response = requests.get(category_url)
    if response.status_code == 200:
        movies = response.json().get('results', [])
        for movie in movies:
            title = movie['title']
            poster_path = movie.get('poster_path')
            if (poster_path):
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

            # Fetch additional movie details
            details = fetch_movie_details(movie['id'])
            movie['runtime'] = details.get('runtime')
            movie['adult'] = details.get('adult', False)

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

# Serve posters

# Start the frontend
def start_frontend():
    frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
    print(f"Frontend path: {frontend_path}")  # Debugging line
    subprocess.Popen(["npm", "start"], cwd=frontend_path)

# Add ourselfs as users
def add_initial_users():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    add_user(1, "Anthonella Alessandra", "Frutos Lara", "1234", "a.frutoslara@stud.uni-goettingen.de", "Admin")
    add_user(2, "Emily Sophie", "Aust", "1234", "emilysophie.aust@stud.uni-goettingen.de", "Client")
    add_user(3, "Cordula", "Maier", "1234", "cordula.maier@stud.uni-goettingen.de", "Client")
    add_user(4, "Matthias", "Schmidt", "1234", "matthias.schmidt@email.de", "Client")

    con.close()

# Add cinema halls
def add_initial_halls():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for i in range(1, 11):
        add_hall(i, f"Kino {i}", 10, 20, 200)
        conn.commit()

    conn.close()

def add_initial_show():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    idList = []
    for row in cur.execute("SELECT id FROM movies WHERE category = ?", ('now_playing',)):
        idList.append(row[0])

    showtime = "16:00 Uhr"
    hall_id = 1
    for i in range(len(idList)):
        if (i % 2 != 0):
            showtime = "20:00 Uhr"
        else:
            showtime = "16:00 Uhr"

        if (i % 2 == 0 and i != 0):
            hall_id += 1

        add_show(None, idList[i], hall_id, showtime)

    con.close()

# add_seat(iD, status, row_number, seat_number, price, reservation_iD, show_iD):
def add_initial_seats():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    id_counter = 1
    for show_id in range(1, 21):
        price = 8
        for row_number in range(1, 11):
            if (row_number >= 5):
                price = 5
            for seat_number in range(1, 21):
                add_seat(id_counter, "free", row_number, seat_number, price, None, show_id)
                id_counter += 1
    con.commit()
    con.close()

def get_db_connection():
    conn = sqlite3.connect("movies.db")
    conn.row_factory = sqlite3.Row
    return conn


if __name__ == "__main__":
    initialize_database()
    fetch_and_save_movies()
    add_initial_users()
    add_initial_halls()
    add_initial_show()
    add_initial_seats()
    start_frontend()
    app.run(debug=True, use_reloader=False)
