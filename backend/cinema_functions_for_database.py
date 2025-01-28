# ***************************************************************************************
# DESCRIPTION

# Here you can find all the functions to call our database. Below you can see our sections,
# for which we have defined functionalities. Below that, you can see an overview of all
# single functions in a 'Table of functions'.


# SECTIONS

# We have all the functions for ...
# a) Adding data
# b) Getting data
#    -> Login functions
# c) Deleting data
# d) Setting/Updating data


# TABLE OF FUNCTIONS

# a) Adding data
# add_movie(iD, year, genre, movie_name, duration, regisseur, bewertung)
# add_user(iD, vorname, nachname, password, email, role)
# ...

# ***************************************************************************************

# Imports
import sqlite3 # Documentation: https://docs.python.org/3/library/sqlite3.html
import requests
import json
import os

# Connecting with our database
con = sqlite3.connect("movies.db")
cur = con.cursor()

# a) Adding data
def add_movie(id, title, release_date, overview, vote_average, poster_path, category, genres, hall_id, showtime):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO movie VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id, title, release_date, overview, vote_average, poster_path, category, genres, hall_id, showtime))
        con.commit()
        print(f"Movie {movie_name} added.")
    except sqlite3.IntegrityError:
        print(f"Error while adding movie: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

# Adding users hint: id = None for using AUTOINCREMENT in SQL
def add_user(iD, vorname, nachname, password, email, role):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO user VALUES
                (?, ?, ?, ?, ?, ?)
        """, (iD, vorname, nachname, password, email, role))
        con.commit()
        print(f"User {vorname} {nachname} added.")
    except sqlite3.IntegrityError:
        print(f"Error while adding user: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

def add_reservation(iD, total_price, time_of_reservation, user_iD, movie_iD):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO reservation VALUES
                (?, ?, ?, ?, ?)
        """, (iD, total_price, time_of_reservation, user_iD, movie_iD))
        con.commit()
        print(f"Reservation {iD} added.")
    except sqlite3.IntegrityError:
        print(f"Error while adding reservation: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

def add_hall(iD, hall_name, row_count, seats_per_row, total_seats):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO hall VALUES
                (?, ?, ?, ?, ?)
        """, (iD, hall_name, row_count, seats_per_row, total_seats))
        con.commit()
        print(f"Hall {hall_name} added.")
    except sqlite3.IntegrityError:
        print(f"Error while adding hall: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

def add_seat(iD, status, row_number, seat_number, price, reservation_iD, hall_iD):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO seat VALUES
                (?, ?, ?, ?, ?, ?, ?)
        """, (iD, status, row_number, seat_number, price, reservation_iD, hall_iD))
        con.commit()
        print(f"Seat {iD} added.")
    except sqlite3.IntegrityError:
        print(f"Error while adding seat: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

def add_logs_history(iD, action, action_timestamp, user_iD, reservation_iD):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO logs_history VALUES
                (?, ?, ?, ?, ?)
        """, (iD, action, action_timestamp, user_iD, reservation_iD))
        con.commit()
        print(f"Logs and history {iD} added.")
    except sqlite3.IntegrityError:
        print(f"Error while adding Logs/History: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

# b) Getting data
def get_all_users():
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM user"):
        print(row)
    con.close()

def get_all_reservations():
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM reservation"):
        print(row)
    con.close()

def get_all_halls():
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM hall"):
        print(row)
    con.close()

def get_all_seats():
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM seat"):
        print(row)
    con.close()

def get_seats_for_hall(hall_id):
    try:
        db_path = os.path.abspath(os.path.join("movies.db"))
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        seats = cur.execute("""SELECT id, status, row_number, seat_number, price, reservation_id FROM seat WHERE hall_id = ? """, (hall_id,)).fetchall()
        print(f"Fetching seats for hall_id={hall_id}")
        print(f"Query result: {seats}")

        return[
            {
                "id": seat[0],
                "status": seat[1],
                "row_number": seat[2],
                "seat_number": seat[3],
                "price": seat[4],
                "isbooked": seat[1] == "booked"
            }
            for seat in seats
        ]
    except sqlite3.Error as e:
        print(f"Error while fetching seats: {e}")
        return []
    finally:
        con.close()

def get_all_movies():
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM movies"):
        print(row)
    con.close()

def get_all_now_playing_movies():
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM movies WHERE category = ?", ('now_playing',)):
        print(row)
    con.close()

def get_all_logs_histories():
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM logs_history"):
        print(row)
    con.close()

def login_check_for_user(email):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM user WHERE email = ?", (email,))
    result = cur.fetchone()
    con.close()
    if result:
        return 1
    else:
        return 0

def login_check_password(email, password):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT password FROM user WHERE email = ?", (email,))
    result = cur.fetchone()
    con.close()
    if result:
        if password == str(result[0]):
            return 1
        else:
            return 0
    else:
        return f"No user found with email {email}"

def get_movie_id(title):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT id FROM movies WHERE title = ?", (title,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    else:
        return None
def get_movie(id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT title FROM movies WHERE id = ?", (id,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    else:
        return None
def get_movie_with_filter():
    return
def get_movie_adult(id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT adult FROM movie WHERE id = ?", (id,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    else:
        return None
def get_movie_genre(id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT genre FROM movies WHERE id = ?", (id,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    else:
        return None

def get_movie_title(id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT title FROM movies WHERE id = ?", (id,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    else:
        return None
def get_movie_overview(id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT overview FROM movies WHERE id = ?", (id,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    else:
        return None
def get_movie_release_date(id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT release_date FROM movies WHERE id = ?", (id,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    else:
        return None
#def get_movie_duration(id):
#    con = sqlite3.connect("movies.db")
#    cur = con.cursor()
#    cur.execute("SELECT  FROM movie WHERE id = ?", (id,))
#    result = cur.fetchone()
#    con.close()
#    if result:
#        return result[0]
#    else:
#        return None
def get_movie_vote_average(id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT vote_average FROM movies WHERE id = ?", (id,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    else:
        return None

def get_posterurl(movie_id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    poster_baseURL = "https://image.tmdb.org/t/p/w500"
    cur.execute("SELECT poster_path FROM movies WHERE id = ?", (movie_id,))
    result = cur.fetchone()
    con.close()
    if result:
        print(poster_baseURL + str(result[0]))
    else:
        return None

def get_user_id(email):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT id FROM user WHERE email = ?", (email,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    else:
        return None

def get_user_vorname(id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT vorname FROM user WHERE id = ?", (id,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    else:
        return None

def get_user_nachname(id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT nachname FROM user WHERE id = ?", (id,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    else:
        return None

def get_user_email(id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT email FROM user WHERE id = ?", (id,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    else:
        return None

def get_user_role(id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT role FROM user WHERE id = ?", (id,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    else:
        return None

# c) Deleting data
def delete_user(user_iD):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("DELETE FROM user WHERE id = ?", (user_iD,))
        con.commit()
        print(f"User with ID {user_iD} deleted.")
    except sqlite3.Error as e:
        print(f"Error while deleting user: {e}")
    finally:
        con.close()

def delete_movie(movie_iD):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("DELETE FROM movies WHERE id = ?", (movie_iD,))
        con.commit()
        print(f"Movie with ID {movie_iD} deleted.")
    except sqlite3.Error as e:
        print(f"Error while deleting movie: {e}")
    finally:
        con.close()

def delete_reservation(reservation_iD):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("DELETE FROM reservation WHERE id = ?", (reservation_iD,))
        con.commit()
        print(f"Reservation with ID {reservation_iD} deleted.")
    except sqlite3.Error as e:
        print(f"Error while deleting reservation: {e}")
    finally:
        con.close()

def delete_hall(hall_iD):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("DELETE FROM hall WHERE id = ?", (hall_iD,))
        con.commit()
        print(f"Hall with ID {hall_iD} deleted.")
    except sqlite3.Error as e:
        print(f"Error while deleting hall: {e}")
    finally:
        con.close()

def delete_seat(seat_iD):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("DELETE FROM seat WHERE id = ?", (seat_iD,))
        con.commit()
        print(f"Seat with ID {seat_iD} deleted.")
    except sqlite3.Error as e:
        print(f"Error while deleting seat: {e}")
    finally:
        con.close()

def delete_logs_history(logs_history_iD):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("DELETE FROM logs_history WHERE id = ?", (logs_history_iD,))
        con.commit()
        print(f"Log/history with ID {logs_history_iD} deleted.")
    except sqlite3.Error as e:
        print(f"Error while deleting Logs/History: {e}")
    finally:
        con.close()

# d) Setting/Updating data

def set_hall_showtime_for_movie(movie_id, hall_id, showtime):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("UPDATE movies SET hall_id = ? WHERE id = ?", (hall_id, movie_id))
        con.commit()
        cur.execute("UPDATE movies SET showtime = ? WHERE id = ?", (showtime, movie_id))
        con.commit()
        if cur.rowcount > 0:
            print(f"Movie with ID {movie_id} updated: hall_id = {hall_id}")
            print(f"Movie with ID {movie_id} updated: showtime = {showtime}")
        else:
            print(f"No movie found with ID {movie_id}.")
    except sqlite3.Error as e:
        print(f"Error while updating movies hall_id and showtime: {e}")
    finally:
        con.close()

def update_user_name(user_id, new_vorname, new_nachname):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("UPDATE user SET vorname = ? WHERE id = ?", (new_vorname, user_id))
        con.commit()
        cur.execute("UPDATE user SET nachname = ? WHERE id = ?", (new_nachname, user_id))
        con.commit()
        if cur.rowcount > 0:
            print(f"User with ID {user_id} updated: name = {new_vorname} {new_nachname}")
        else:
            print(f"No user found with ID {user_id}.")
    except sqlite3.Error as e:
        print(f"Error while updating users name: {e}")
    finally:
        con.close()

def update_user_email(user_id, new_email):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("UPDATE user SET email = ? WHERE id = ?", (new_email, user_id))
        con.commit()
        if cur.rowcount > 0:
            print(f"User with ID {user_id} updated: email = {new_email}")
        else:
            print(f"No user found with ID {user_id}.")
    except sqlite3.Error as e:
        print(f"Error while updating users email: {e}")
    finally:
        con.close()

# Hint: only Admins can change user roles!
def update_user_role(user_id, new_role):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("UPDATE user SET role = ? WHERE id = ?", (new_role, user_id))
        con.commit()
        if cur.rowcount > 0:
            print(f"User with ID {user_id} updated: role = {new_role}")
        else:
            print(f"No user found with ID {user_id}.")
    except sqlite3.Error as e:
        print(f"Error while updating users role: {e}")
    finally:
        con.close()

def update_seat_status(hall_id, seat_iD, new_status):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("UPDATE seat SET status = ? WHERE hall_id = ? AND id = ?", (new_status, hall_id, seat_iD))
        con.commit()
        # rowcount is number of changed rows while updating
        if cur.rowcount > 0:
            print(f"Seat with ID {seat_iD} in hall {hall_id} updated: status = {new_status}")
        else:
            print(f"No seat found with ID {seat_iD}.")
    except sqlite3.Error as e:
        print(f"Error while updating seat status: {e}")
    finally:
        con.close()

def calculate_total_price(hall_id):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("SELECT sum(price) FROM seat WHERE status = 'selected'")
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return None
    except sqlite3.Error as e:
        print(f"Error while calculating total price: {e}")
    finally:
        con.close()

