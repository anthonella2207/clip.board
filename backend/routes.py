from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, request, jsonify
import sqlite3
from flask_cors import cross_origin, CORS
from cinema_functions_for_database import *

#connection to our database
def get_db_connection():
    con = sqlite3.connect('movies.db')
    con.row_factory = sqlite3.Row
    print("Datenbank verbunden:", 'movies.db')  # Ausgabe zur Bestätigung
    return con

#Login routes
auth_routes = Blueprint('auth', __name__)
CORS(auth_routes)

@auth_routes.route('/login', methods=['POST'])
@cross_origin()
def login():
    try:
        data = request.get_json()

        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({"success": False, "message": "Missing email or password"}), 400

        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM user WHERE TRIM(email) = ?", (email.strip(),))
        user = cur.fetchone()
        con.close()

        if user:
            if user["password"] == password:
                return jsonify({"success": True, "message": "Login Successful", "role": user["role"]})
            else:
                return jsonify({"success": False, "message": "wrong password"}), 401
        else:
            return jsonify({"success": False, "message": "email not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500

#sign-up route

@auth_routes.route('/signup', methods=['POST'])
@cross_origin()
def signup():
    data = request.get_json()
    first_name = data.get("vorname")
    last_name = data.get("nachname")
    email = data.get('email')
    password = data.get('password')

    #make sure all fields are filled in
    if not (first_name and last_name and email and password):
        return jsonify({"success": False, "message": "missing fields"}), 400
    con = get_db_connection()
    cur = con.cursor()

    #check if user already exists
    cur.execute("SELECT * FROM user WHERE email = ?", (email,))
    if cur.fetchone():
        con.close()
        return jsonify({"success": False, "message": "email already registered"}), 400

    role = "Client"

    cur.execute("""
    INSERT INTO user (email, password, vorname, nachname, role)VALUES(?, ?, ?, ?, ?)""",
                (email, password, first_name, last_name, role))

    con.commit()
    con.close()

    return jsonify({"success": True, "message": "Registration successful"}), 201

#seats for halls routes

seats_routes = Blueprint('seats', __name__)

@seats_routes.route("/api/seats/<int:show_id>", methods=['GET'])
@cross_origin()
def get_seats(show_id):
    try:
        seats = get_seats_for_show(show_id)
        return jsonify({"seats": seats})
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

#route for reservation

#route for filters

movies_routes = Blueprint('movies', __name__)
@movies_routes.route("/api/movies/now_playing", methods=['GET'])
@cross_origin()
def get_filtered_movies():
    try:
        genres = request.args.get("genres")
        vote_average = request.args.get("vote_average")
        duration = request.args.get("duration")
        keywords = request.args.get("keywords")

        movies = filter_movies(genres=genres, duration=duration, keywords=keywords)

        formatted_movies = [
            {
                "id": movie[0],
                "title": movie[1],
                "release_date": movie[2],
                "overview": movie[3],
                "vote_average": movie[4],
                "poster_path": movie[5],
                "category": movie[6],
                "genres": movie[7],
                "runtime": movie[8],
                "vote_count": movie[9]
            }
            for movie in movies
        ]
        return jsonify({"success": True, "movies": formatted_movies}), 200

    except Exception as e:
        return jsonify({"success": False, "message": "server error", "error": str(e)}), 500

#route for genres

@movies_routes.route("/api/genres", methods=['GET'])
def get_available_genres():
    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT genres FROM movies")
        all_genres = cur.fetchall()

        unique_genres = set()

        for row in all_genres:
            if row[0]:
                genres = row[0].split(", ")  # Splitten in einzelne Genres
                unique_genres.update(genres)

        con.close()

        return jsonify({"genres": sorted(list(unique_genres))})

    except Exception as e:
        return jsonify({"success": False, "message": "server error", "error": str(e)}), 500

#route for logout