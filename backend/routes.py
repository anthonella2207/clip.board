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
        cur.execute("SELECT id, password, role, vorname, nachname FROM user WHERE TRIM(email) = ?", (email,))
        user = cur.fetchone()
        con.close()

        if user:
            user_id, stored_password, role, first_name, last_name = user
            if stored_password == password:
                return jsonify({
                    "success": True,
                    "message": "Login Successful",
                    "user_id": user_id,
                    "role": role,
                    "first_name": first_name,
                    "last_name": last_name
                    })
            else:
                return jsonify({"success": False, "message": "wrong password"}), 401
        else:
            return jsonify({"success": False, "message": "email not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500

#route for user updating password and email --------------------------------------------------

@auth_routes.route('update_email', methods=['POST'])
@cross_origin()

def update_email():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        new_email = data.get("new_email")
        password = data.get("password")

        if not (user_id and new_email and password):
            return jsonify({"success": False, "message": "Missing fields"}), 400

        #Verify user with password

        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT password FROM user WHERE id = ?", (user_id,))
        user = cur.fetchone()
        con.close()

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        stored_password = user["password"]
        if stored_password != password:
            return jsonify({"success": False, "message": "Wrong password"}), 401

        update_user_email(user_id, new_email)
        return jsonify({"success": True, "message": "Email updated successfully"})

    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500

@auth_routes.route('/update_password', methods=['POST'])
@cross_origin()

def update_password():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if not (user_id and old_password and new_password):
            return jsonify({"success": False, "message": "Missing fields"}), 400

        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT password FROM user WHERE id = ?", (user_id,))
        user = cur.fetchone()
        con.close()

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        stored_password = user[0]
        if stored_password != old_password:
            return jsonify({"success": False, "message": "Wrong password"}), 401

        update_user_password(user_id, new_password)
        return jsonify({"success": True, "message": "Password updated successfully"})

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

    cur.execute("SELECT id FROM user WHERE email = ?", (email,))
    user_id = cur.fetchone()[0]

    con.close()
    return jsonify({"success": True, "message": "Registration successful", "user_id": user_id}), 201

#route stats hall occupancy

@auth_routes.route('/api/hall_occupancy', methods=['GET'])
@cross_origin()
def get_hall_occupancy():
    """ Berechnet die Saalauslastung für jede Show """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT s.showtime, h.name AS hall, 
               COUNT(*) AS total_seats,
               SUM(CASE WHEN seat.status = 'booked' THEN 1 ELSE 0 END) AS booked_seats,
               ROUND(SUM(CASE WHEN seat.status = 'booked' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS occupancy_rate
        FROM seat
        JOIN shows s ON seat.show_id = s.id
        JOIN hall h ON s.hall_id = h.id
        GROUP BY s.showtime, h.name
        ORDER BY occupancy_rate DESC;
    """)

    data = [
        {"showtime": row[0], "hall": row[1], "total_seats": row[2], "booked_seats": row[3], "occupancy_rate": row[4]}
        for row in cur.fetchall()]

    con.close()
    return jsonify(data)


@auth_routes.route('/api/monthly_revenue', methods=['GET'])
@cross_origin()
def get_monthly_revenue():
    """ Berechnet die Einnahmen pro Monat """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT strftime('%Y-%m', r.time_of_reservation) AS month,
               SUM(r.total_price) AS revenue
        FROM reservation r
        GROUP BY month
        ORDER BY month DESC;
    """)

    data = [{"month": row[0], "revenue": row[1]} for row in cur.fetchall()]

    con.close()
    return jsonify(data)


@auth_routes.route('/api/bestseller_movies', methods=['GET'])
@cross_origin()
def get_bestseller_movies():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT m.title, COUNT(seat.id) AS ticket_count
        FROM movies AS m
        JOIN shows AS s ON m.id = s.movie_id
        JOIN seat AS seat ON seat.show_id = s.id
        WHERE seat.status = 'booked'
        GROUP BY m.title
        ORDER BY ticket_count DESC
        LIMIT 3;
    """)

    data = [{"title": row[0], "count": row[1]} for row in cur.fetchall()]
    con.close()
    return jsonify(data)

#routes for show statistics

@auth_routes.route('/api/show_stats', methods=['GET'])
@cross_origin()

def get_show_stats():
    try:
        show_id = request.args.get('show_id')
        if not show_id:
            return jsonify({"success": False, "message": "Missing show_id"}), 400

        available = calculate_number_available_seats(show_id)
        booked = calculate_number_not_available_seats(show_id)

        con = get_db_connection()
        cur = con.cursor()
        cur.execute("""
            SELECT SUM(s.price) 
            FROM seat s
            JOIN reservation r ON s.reservation_id = r.id
            WHERE r.show_id = ?
        """, (show_id,))

        revenue = cur.fetchone()[0] or 0
        con.close()

        return jsonify({
            "success": True,
            "available_seats": available,
            "booked_seats": booked,
            "revenue": revenue,
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500


@auth_routes.route('/api/user_logs', methods=['GET'])
@cross_origin()
def get_all_logs_histories():
    try:
        con = get_db_connection()
        cur = con.cursor()

        user_id = request.args.get("user_id")
        action_filter = request.args.get("action")

        query = """
            SELECT lh.id, lh.action, lh.action_timestamp, u.vorname, u.nachname 
            FROM logs_history lh 
            JOIN user u ON lh.user_id = u.id
        """
        params = []

        if user_id:
            query += " WHERE lh.user_id = ?"
            params.append(user_id)

        if action_filter:
            if user_id:
                query += " AND lh.action = ?"
            else:
                query += " WHERE lh.action = ?"
            params.append(action_filter)

        query += " ORDER BY lh.action_timestamp DESC"

        cur.execute(query, params)
        logs = [{"id": row[0], "action": row[1], "timestamp": row[2], "user": f"{row[3]} {row[4]}"} for row in
                cur.fetchall()]

        con.close()
        return jsonify(logs)
    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500


#route for deleting

@auth_routes.route('/api/delete_reservation', methods=['DELETE'])
@cross_origin()
def delete_reservation():
    try:
        seat_id = request.args.get("seat_id")
        if not seat_id:
            return jsonify({"success": False, "message": "Seat ID missing"}), 400

        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT reservation_id FROM seat WHERE id = ?", (seat_id,))
        reservation_id = cur.fetchone()

        if not reservation_id:
            return jsonify({"success": False, "message": "Reservation not found"}), 404

        reservation_id = reservation_id[0]

        cur.execute("UPDATE seat SET reservation_id = NULL, status = 'free' WHERE id = ?", (seat_id,))

        cur.execute("SELECT COUNT(*) FROM seat WHERE reservation_id = ?", (reservation_id,))
        remaining_seats = cur.fetchone()[0]

        if remaining_seats == 0:
            cur.execute("DELETE FROM reservation WHERE id = ?", (reservation_id,))

        con.commit()
        con.close()

        return jsonify({"success": True, "message": "Reservation deleted"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500


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


#route for available shows -----------------------------------------------------------------

@seats_routes.route("/api/available_shows", methods=['GET'])
@cross_origin()

def get_available_shows():
    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT DISTINCT show_id FROM seat")
        show_ids = [row[0] for row in cur.fetchall()]
        con.close()

        return jsonify({"success": True, "available_shows": show_ids}), 200

    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500

#route for reservation ---------------------------------------------------------------------

@seats_routes.route("/api/reserve", methods=['POST'])
@cross_origin()

def reserve_seats():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        show_id = data.get('show_id')
        seat_ids = data.get('seat_ids')

        if not user_id or not show_id or not seat_ids:
            return jsonify({"Success": False, "message": "missing user_id, show_id or seat_ids"}), 400

        available = is_seat_available(seat_ids)
        if not available:
            return jsonify({"Success": False, "message": "one or more seats are already reserved"}), 400

        total_price = calculate_total_price(seat_ids, show_id) or 0.00

        reservation_id = add_reservation(None, total_price, datetime.now(), user_id, show_id)

        if not reservation_id:
            return jsonify({"success": False, "message": "Reservation failed"}), 500

        for seat_id in seat_ids:
            update_seat_reservation_id_and_status(seat_id, reservation_id)

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

#route for add_logs ----------------------------------------------------------------------------

@auth_routes.route('/add_log', methods=['POST'])
@cross_origin()
def add_log():
    try:
        data = request.get_json()
        action = data.get("action")
        user_id = data.get("user_id")
        reservation_id = data.get("reservation_id", None)  # Optional

        if not action or not user_id:
            return jsonify({"success": False, "message": "Missing data"}), 400

        print(f"🔍 Debug: add_logs_history({repr('User made a reservation')}, {repr(user_id)}, {repr(reservation_id)})")

        add_logs_history(action, user_id, reservation_id)
        return jsonify({"success": True, "message": "Log added"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500
