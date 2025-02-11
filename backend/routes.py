from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, request, jsonify
import sqlite3
from flask_cors import cross_origin, CORS
from cinema_functions_for_database import *

#connection to our database ------------------------------------------------------
def get_db_connection():
    con = sqlite3.connect('movies.db')
    con.row_factory = sqlite3.Row
    print("Datenbank verbunden:", 'movies.db')  # Ausgabe zur Bestätigung
    return con

#Login routes --------------------------------------------------------------------
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
        cur.execute("SELECT id, password, role FROM user WHERE TRIM(email) = ?", (email,))
        user = cur.fetchone()
        con.close()

        if user:
            user_id, stored_password, role = user
            if stored_password == password:
                return jsonify({"success": True, "message": "Login Successful", "user_id": user_id, "role": user["role"]})
            else:
                return jsonify({"success": False, "message": "wrong password"}), 401
        else:
            return jsonify({"success": False, "message": "email not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500

#sign-up route -------------------------------------------------------------------------------

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

#seats for halls routes-------------------------------------------------------------------------

seats_routes = Blueprint('seats', __name__)

@seats_routes.route("/api/seats/<int:show_id>", methods=['GET'])
@cross_origin()
def get_seats(show_id):
    try:
        seats = get_seats_for_show(show_id)
        return jsonify({"seats": seats})
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

#route for reservation ---------------------------------------------------------------------

@seats_routes.route("/api/reserve", methods=['POST'])
@cross_origin()

def reserve_seats():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        show_id = data.get('show_id')
        seat_ids = data.get('seat_ids')

        print(f"🔹 Reservierung erhalten: user_id={user_id}, show_id={show_id}, seat_ids={seat_ids}")

        if not user_id or not show_id or not seat_ids:
            print("❌ Fehlende Parameter: user_id, show_id oder seat_ids fehlen!")
            return jsonify({"Success": False, "message": "missing user_id, show_id or seat_ids"}), 400

        available = is_seat_available(seat_ids)
        if not available:
            print("❌ Einige Sitze sind bereits reserviert!")
            return jsonify({"Success": False, "message": "one ore more seats are already reserved"}), 400

        total_price = calculate_total_price(seat_ids, show_id)
        print(f"🔹 Berechneter Gesamtpreis: {total_price}")

        reservation_id = add_reservation(None, total_price, datetime.now(), user_id, show_id)

        if not reservation_id:
            print("❌ Fehler: reservation_id ist None! Reservierung fehlgeschlagen.")
            return jsonify({"success": False, "message": "Reservation failed"}), 500

        for seat_id in seat_ids:
            update_seat_reservation_id_and_status(seat_id, reservation_id)

        print(f"✅ Reservierung erfolgreich: ID {reservation_id}")
        return jsonify({"success": True, "reservation_id": reservation_id, "total_price": total_price}), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "error": str(e)}), 500

#route for filters ------------------------------------------------------------------------------------

movies_routes = Blueprint('movies', __name__)
@movies_routes.route("/api/movies/now_playing", methods=['GET'])
@cross_origin()
def get_filtered_movies():
    try:
        genres = request.args.get("genres")
        vote_average = request.args.get("vote_average")
        duration = request.args.get("duration")
        keywords = request.args.get("keywords")

        vote_threshold = None
        if vote_average and vote_average.startswith(">"):
            try:
                vote_threshold = float(vote_average[1:])  # removes ">"
            except ValueError:
                pass

        movies = filter_movies(genres=genres, vote_average=vote_threshold, duration=duration, keywords=keywords)

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

#route for genres -------------------------------------------------------------------------------------

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

#route for logout ------------------------------------------------------------------------------

@auth_routes.route('/logout', methods=['POST'])
@cross_origin()
def logout():
    try:
        return jsonify({"success": True, "message": "User logged out successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": "server error", "error": str(e)}), 500