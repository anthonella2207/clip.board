POSTER_FOLDER = "./posters"
from flask import Blueprint, request, jsonify, send_from_directory
import sqlite3
import re
from flask_cors import cross_origin, CORS
from cinema_functions_for_database import *

#connection to our database ------------------------------------------------------
def get_db_connection():
    con = sqlite3.connect('movies.db')
    con.row_factory = sqlite3.Row
    print("Datenbank verbunden:", 'movies.db')  # Ausgabe zur Bestätigung
    return con

#----Auth-Routes---------------------------------------------------------------------

""" This function handles the login by getting the user's email and password from a
POST- request, then checks if the user exists in the database, checks if the entered 
password matches the stored password and returns errors if the password is wrong, 
the email does not exist or some other error occurs. """

auth_routes = Blueprint('auth', __name__)
CORS(auth_routes)

@auth_routes.route('/login', methods=['POST'])
@cross_origin()
def login():
    try:
        data = request.get_json()

        #getting email and password from POST-request
        email = data.get('email', '').strip()
        password = data.get('password', '')

        #if one of the fields is empty, return
        if not email or not password:
            return jsonify({"success": False, "message": "Missing email or password"}), 400

        #connection to database
        con = get_db_connection()
        cur = con.cursor()

        #if email matches, choose id, password, role, first name, last name from database table
        cur.execute("SELECT id, password, role, vorname, nachname FROM user WHERE TRIM(email) = ?", (email,))

        #gets first line as tuple "user"
        user = cur.fetchone()
        con.close()

        #if user user exists
        if user:
            user_id, stored_password, role, first_name, last_name = user

            #check if entered password matches stored password
            if stored_password == password:
                return jsonify({
                    "success": True,
                    "message": "Login Successful",
                    "user_id": user_id,
                    "email": email,
                    "role": role,
                    "first_name": first_name,
                    "last_name": last_name
                    })

            #if password wrong return 401 unauthorized
            else:
                return jsonify({"success": False, "message": "wrong password"}), 401

        #if email does not exist in database, return 404 not found
        else:
            return jsonify({"success": False, "message": "email not found"}), 404

    #if error occurs, return generic server error 500
    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500


"""This function handles the logout. It is called if a POST-request is sent.  If the logout
is successful, it returns 200 (successful logout). Else an internal server error is returned."""

@auth_routes.route('/logout', methods=['POST'])
@cross_origin()
def logout():
    try:
        return jsonify({"success": True, "message": "User logged out successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": "server error", "error": str(e)}), 500


"""This function handles the sign-up of a new user. It gets the data first name, last name,
email and password via POST-request, extracts it and saves it to the database. The function
checks if every field is filled and else returns an error. It also checks if the email 
format is valid, if the user already exists and sets the user's role to Client. It saves 
the password to the database and gets the user_id of the new registered user."""

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

    #check if entered email is valid
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
    if not re.match(email_regex, email):
        return jsonify({"success": False, "message": "Invalid email format"}), 400

    #check if user already exists
    cur.execute("SELECT * FROM user WHERE email = ?", (email,))
    if cur.fetchone():
        con.close()
        return jsonify({"success": False, "message": "email already registered"}), 400

    role = "Client"

    add_user(None, email, password, first_name, last_name, role)

    con.commit()

    cur.execute("SELECT id FROM user WHERE email = ?", (email,))
    user_id = cur.fetchone()[0]

    con.close()
    return jsonify({"success": True, "message": "Registration successful", "user_id": user_id}), 201


"""This function updates the email of a user. It gets user_id, the new email and the password
from JSON-body. It checks if the user filled in every field and gets the password from the 
database. It checks if the user exists in the database and compares the entered password with
the stored password. Then it calls the function update_user_email, to store the updated email
in the database."""

@auth_routes.route('/update_email', methods=['POST'])
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


"""This function updates the password of the user. It gets user_id, old password and new password 
from JSON-body, then checks if any fields are missing (if so, returns error). It checks if the
user exists in the database and compares the stored password to the entered password.. Calls function
update_user_password, to store the new password in the database."""

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


"""This function gets the hall occupancy from the database. It checks if the Client requests
a specific show, if show_id is missing, all shows are retrieved. It selects the show_id, 
showtime and hall_name from the database and if show_id is given, it filters only this show. 
Then it calculates the occupancy for each show and the revenue if a specific show is requested
All data for a show is stored in a dict, if specific show is requested, revenue also stored
in dict."""

@auth_routes.route('/api/hall_occupancy', methods=['GET'])
@cross_origin()
def get_hall_occupancy():
    try:
        show_id = request.args.get('show_id')

        con = get_db_connection()
        cur = con.cursor()

        if show_id:
            cur.execute("""
                SELECT s.id, s.showtime, h.name
                FROM shows s
                JOIN hall h ON s.hall_id = h.id
                WHERE s.id = ?
            """, (show_id,))
        else:
            cur.execute("""
                SELECT s.id, s.showtime, h.name
                FROM shows s
                JOIN hall h ON s.hall_id = h.id
            """)

        shows = cur.fetchall()
        con.close()

        if show_id and not shows:
            return jsonify({"success": False, "message": "Show not found"}), 404

        occupancy_data = []

        for show in shows:
            sid = show[0]
            showtime = show[1]
            hall_name = show[2]

            available_seats = calculate_number_available_seats(sid) or 0
            total_seats = (calculate_number_available_seats(sid) or 0) + (calculate_number_not_available_seats(sid) or 0)
            booked_seats = calculate_number_not_available_seats(sid) or 0
            occupancy_rate = (booked_seats / total_seats * 100) if total_seats > 0 else 0

            revenue = None
            if show_id:
                con = get_db_connection()
                cur = con.cursor()
                cur.execute("""
                    SELECT SUM(s.price) 
                    FROM seat s
                    JOIN reservation r ON s.reservation_id = r.id
                    WHERE r.show_id = ?
                """, (sid,))
                revenue = cur.fetchone()[0] or 0
                con.close()

            show_data = {
                "showtime": showtime,
                "hall": hall_name,
                "total_seats": total_seats,
                "available_seats": available_seats,
                "booked_seats": booked_seats,
                "occupancy_rate": round(occupancy_rate, 2)
            }
            if show_id:
                show_data["revenue"] = revenue

            occupancy_data.append(show_data)

        return jsonify(occupancy_data), 200

    except sqlite3.Error as db_error:
        return jsonify({"success": False, "message": "Database error", "error": str(db_error)}), 500

    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500


"""This function calculates the monthly revenue of the cinema based on the reservations. 
It sends a request to the database, converts date of reservation to format: YYYY-MM, then
calculates revenue per month, chooses dates from reservation table, makes sure to only 
consider reservations with at least one seat, groups results by month and sorts results
descending. Then returns a list of dicts with month and revenue."""

@auth_routes.route('/api/monthly_revenue', methods=['GET'])
@cross_origin()
def get_monthly_revenue():
    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("""
            SELECT strftime('%Y-%m', r.time_of_reservation) AS month,
                   SUM(r.total_price) AS revenue
            FROM reservation r
            WHERE EXISTS (SELECT 1 FROM seat WHERE seat.reservation_id = r.id)
            GROUP BY month
            ORDER BY month DESC;
        """)

        data = [{"month": row[0], "revenue": row[1]} for row in cur.fetchall()]
        return jsonify(data), 200

    except sqlite3.Error as db_error:
        return jsonify({"success": False, "message": "Database error", "error": str(db_error)}), 500

    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500

    finally:
        if 'con' in locals():
            con.close()


"""This function gets the three best selling movies. It requests the movie titles and the number
of sold tickets, only considers booked seats that belong to a reservation, groups data by movie
titles, sorts number of sold tickets descending and returns the top three movies. It converts the
results to a list of dicts and returns it as JSON-object."""

@auth_routes.route('/api/bestseller_movies', methods=['GET'])
@cross_origin()
def get_bestseller_movies():
    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("""
            SELECT m.title, COUNT(seat.id) AS ticket_count 
            FROM movies AS m
            JOIN shows AS s ON m.id = s.movie_id
            JOIN seat AS seat ON seat.show_id = s.id
            WHERE seat.status = 'booked' AND seat.reservation_id IS NOT NULL
            GROUP BY m.title
            ORDER BY ticket_count DESC
            LIMIT 3;
        """)

        data = [{"title": row[0], "count": row[1]} for row in cur.fetchall()]
        con.close()
        return jsonify(data)

    except sqlite3.Error as db_error:
        return jsonify({"success": False, "message": "Database error", "error": str(db_error)}), 500

    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500

    finally:
        if 'con' in locals():
            con.close()


"""This functions gets user's activities, such as login, logout, sign up and reservations.
It has an option to filter by user_id and by action. It sorts the logs descending. It returns
the user_id, action, timestamp and user."""

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


"""This function allows to delete a reservation or booked seats based on the seat_id. It gets a
seat_id and checks if this id exists. It gets reservation_id to check if the seat is reserved.
Then it changes the status of the selected seat to free and the reservation_id to null. The selected 
seat_id is updated. It checks if other seat_ids are associated with the reservation_id, if not the
reservation is deleted."""

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

        reservation_id = reservation_id[0] if reservation_id else None
        if not reservation_id:
            return jsonify({"success": False, "message": "Reservation not found"}), 404

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


"""This function enables the user to cancel a reservation. It gets the booking_id from JSON-body.
It looks for a reservation with this id and sets all seats associated with it to free,
reservation_id is set to null and the reservation is deleted from the database."""

@auth_routes.route("/api/bookings/cancel", methods=["DELETE"])
@cross_origin()
def cancel_booking():
    try:
        data = request.get_json()
        booking_id = data.get("booking_id")

        if not booking_id:
            return jsonify({"success": False, "message": "Missing booking_id"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM reservation WHERE id = ?", (booking_id,))
        reservation = cursor.fetchone()

        if not reservation:
            return jsonify({"success": False, "message": "Reservation not found"}), 404

        # set all seats to 'free'
        cursor.execute("UPDATE seat SET reservation_id = NULL, status = 'free' WHERE reservation_id = ?", (booking_id,))
        conn.commit()

        # delete reservation
        cursor.execute("DELETE FROM reservation WHERE id = ?", (booking_id,))

        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Reservation cancelled"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500


"""This function returns all available shows with titles. It connects the movies table
with the shows table to get the movie title for each show. It returns a list of dicts
containing the show_id and the movie title."""

@auth_routes.route('/api/available_shows', methods=['GET'])
@cross_origin()
def get_available_shows():
    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("""
            SELECT s.id, m.title
            FROM shows s
            JOIN movies m ON s.movie_id = m.id
            ORDER BY s.id;
        """)

        shows = [{"show_id": row[0], "title": row[1]} for row in cur.fetchall()]
        con.close()
        return jsonify({"available_shows": shows})

    except sqlite3.Error as db_error:
        return jsonify({"success": False, "message": "Database error", "error": str(db_error)}), 500

    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500


"""This function creates a new log entry to the database. It gets the JSON-body of the request
containing the action, the user_id (and the reservation_id). It calls add_logs_history
to create an entry to the database."""

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

        add_logs_history(action, user_id, reservation_id)
        return jsonify({"success": True, "message": "Log added"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500


"""This function returns all bookings of a specific user. It gets the following data about
the user: reservation_id, movie title, show time, hall, price and sorts the bookings
descending. It converts the data to JSON format and returns it."""

@auth_routes.route("/api/bookings/<int:user_id>", methods=["GET"])
def get_user_bookings(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.id, m.title AS movie_name, s.showtime AS show_time, 
               h.name AS hall, r.total_price AS price
        FROM reservation r
        JOIN shows s ON r.show_id = s.id
        JOIN movies m ON s.movie_id = m.id
        JOIN hall h ON s.hall_id = h.id
        WHERE r.user_id = ?
        ORDER BY s.showtime DESC
    """, (user_id,))

    bookings = [
        {
            "id": row[0],
            "movie_name": row[1],
            "show_time": row[2],
            "hall": row[3],
            "price": row[4]
        }
        for row in cursor.fetchall()
    ]

    conn.close()

    if not bookings:
        return jsonify({"success": True, "bookings": [], "message": "No bookings found"}), 200

    return jsonify({"success": True, "bookings": bookings}), 200


#----seats_routes-------------------------------------------------------------------------------

seats_routes = Blueprint('seats', __name__)

"""This function returns all seats for a specific show. It calls the function get_seats_for_show
and returns a JSON-list of the seats."""

@seats_routes.route("/api/seats/<int:show_id>", methods=['GET'])
@cross_origin()
def get_seats(show_id):
    try:
        seats = get_seats_for_show(show_id)
        return jsonify({"seats": seats})
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


"""This function enables the user to book multiple seats for a show. It gets a JSON request
containing the user_id, show_id and the seat_id's. It checks if the seats are already booked,
calculates the total price of all selected seats and adds a new reservation to the database.
Then it links the seats to the reservation and sets the seats to 'booked'."""

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

#----movies_routes------------------------------------------------------------------------------------

"""This function filters the 'now_playing_movies' based on genre, duration, rating and keywords.
It gets the parameters genre, vote_average, duration or keyword. It converts the vote_average 
value to float (if it starts with '>'), then gets the movies based on the applied filters from
the database. It converts the data to JSON and returns it."""

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


"""This function returns a list of unique genres. It gets all values from column 'genre' in movies
table and extracts the unique genres. It sorts them alphabetically and returns them."""

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
                genres = row[0].split(", ")
                unique_genres.update(genres)

        con.close()

        return jsonify({"genres": sorted(list(unique_genres))})

    except Exception as e:
        return jsonify({"success": False, "message": "server error", "error": str(e)}), 500


"""This function returns the show times of a specific movie. It gets the hall, the show time,
the showTimeId and links the show table with the hall table to get the names of the halls."""

@movies_routes.route("/api/showtimes/<int:movie_id>", methods=["GET"])
def get_showtimes(movie_id):
    conn = get_db_connection()
    showtimes = conn.execute("""
        SELECT h.name AS hall, s.showtime, s.id AS showtimeId
        FROM shows s
        JOIN hall h ON s.hall_id = h.id
        WHERE s.movie_id = ?
        ORDER BY s.showtime ASC
    """, (movie_id,)).fetchall()
    conn.close()

    return jsonify([
        {"hall": row["hall"], "showtime": row["showtime"], "showtimeId": row["showtimeId"]}
        for row in showtimes
    ])


"""This function returns all movies of a specific category (top rated, now playing, upcoming).
It requests the movie_id, movie title, release date, overview, average voting, poster path,
list of genres, runtime and returns them as JSON."""

@movies_routes.route('/api/movies/<category>', methods=['GET'])
def get_movies_by_category(category):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, release_date, overview, vote_average, poster_path, genres, runtime, adult
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
            "genres": movie[6],
            "runtime": movie[7],
            "adult": movie[8]
        }
        for movie in movies
    ])


"""This function returns the poster for a movie."""

@movies_routes.route('/posters/<filename>')
def get_poster(filename):
    return send_from_directory(POSTER_FOLDER, filename)
