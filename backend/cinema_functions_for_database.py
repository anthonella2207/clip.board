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
#    -> Filter functions
# c) Deleting data
# d) Setting/Updating data


# TABLE OF FUNCTIONS

# a) Adding data
# line: 103; add_movie(iD, year, genre, movie_name, duration, regisseur, bewertung)
# line: 121; add_user(iD, vorname, nachname, password, email, role)
# line: 138; add_show(id, movie_id, hall_id, showtime)
# line: 155; add_reservation(id, total_price, time_of_reservation, user_id, show_id)
# line: 172; add_hall(iD, hall_name, row_count, seats_per_row, total_seats)
# line: 189; add_seat(id, status, row_number, seat_number, price, reservation_id, show_iD)
# line: 206; add_logs_history(iD, action, action_timestamp, user_iD, reservation_iD)

# b) getting data
# line: 224; get_all_users()
# line: 232; get_all_reservations()
# line: 240; get_all_halls()
# line: 248; get_all_shows()
# line: 256; get_all_seats()
# line: 264; get_seats_for_show(show_id)
# line: 289; get_all_movies()
# line: 297; get_all_now_playing_movies()
# line: 305; get_all_logs_histories()
# line: 313; login_check_for_user(email)
# line: 324: login_check_password(email, password)
# line: 338; get_movie_id(title)
# line: 348; get_movie(id)
# line: 359; get_movie_adult(id)
# line: 370; get_movie_runtime(id)
# line: 381; get_movie_genre(id)
# line: 392; get_movie_title(id)
# line: 402; get_movie_overview(id)
# line: 412; get_movie_release_date(id)
# line: 423; get_movie_vote_average(id)
# line: 434; get_movie_category(id)
# line: 445; get_posterurl(movie_id)
# line: 457; get_user_id(email)
# line: 468; get_user_vorname(id)
# line: 479; get_user_nachname(id)
# line: 490; get_user_email(id)
# line: 501; get_user_role(id)
# line: 515; filter_movies_by_genres(genres)
# line: 549; filter_movies_by_vote_average(vote_average)
# line: 574; filter_movies_by_duration(duration)
# line: 595; filter_movies_by_keywords(keywords)
# line: 624; filter_movies(genres=None, vote_average=None, duration=None, keywords=None)

#c) deleting data
# line: 687; delete_user(user_iD)
# line: 699; delete_movie(movie_iD)
# line: 711; delete_reservation(reservation_iD)
# line: 723; delete_hall(hall_iD)
# line: 735; delete_seat(seat_iD)
# line: 747; delete_logs_history(logs_history_iD)

#d) setting/updating data
# line: 761; update_user_name(user_id, new_vorname, new_nachname)
# line: 778; update_user_email(user_id, new_email)
# line: 794; update_user_role(user_id, new_role)
# line: 809; update_seat_status(seat_id, new_status, reservation_id = None)
# line: 829; calculate_total_price(seat_ids, show_id)
# line: 857; check_for_admin(user_id)
# line: 875; calculate_number_available_seats(show_id)
# line: 888; calculate_number_not_available_seats(show_id)
# line: 901; calculate_percentage_available_seats(show_id)
# line: 907; calculate_percentage_not_available_seats(show_id)
# line: 913; list_of_available_seats(show_id)
# line: 925; list_of_not_available_seats()
# line: 938; number_of_users_with_information()
# line: 958; pie_chart_seats(show_id)

# ***************************************************************************************

# Imports
import sqlite3 # Documentation: https://docs.python.org/3/library/sqlite3.html
import requests
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime

# Connecting with our database
con = sqlite3.connect("movies.db")
cur = con.cursor()

# a) Adding data
def add_movie(id, title, release_date, overview, vote_average, poster_path, category, genres, runtime, adult):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO movie VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id, title, release_date, overview, vote_average, poster_path, category, genres, runtime, adult))
        con.commit()
        print(f"Movie {title} added.")
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

        add_logs_history(None, "User Added", datetime.now(), None, None)
        con.commit()

    except sqlite3.IntegrityError:
        print(f"Error while adding user: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

def add_show(id, movie_id, hall_id, showtime):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO shows VALUES
                (?, ?, ?, ?)
        """, (id, movie_id, hall_id, showtime))
        con.commit()
        print(f"Show ({id}, {movie_id}, {hall_id}, {showtime}) added.")
    except sqlite3.IntegrityError:
        print(f"Error while adding show: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

def add_reservation(id, total_price, time_of_reservation, user_id, show_id):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO reservation VALUES
                (?, ?, ?, ?, ?)
        """, (id, total_price, time_of_reservation, user_id, show_id))
        con.commit()
        print(f"Reservation {id} added.")

        # Insert reservation action into Logs/history
        # Add History
        add_logs_history(None, "Seat reservation", datetime.now(), user_id, id)
        con.commit()

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

def add_seat(id, status, row_number, seat_number, price, reservation_id, show_iD):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO seat VALUES
                (?, ?, ?, ?, ?, ?, ?)
        """, (id, status, row_number, seat_number, price, reservation_id, show_iD))
        con.commit()
        print(f"Seat {id} added.")
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
    print("User: ID, First Name, Last Name, Password, E-Mail, Role")
    for row in cur.execute("SELECT * FROM user"):
        print(row)
    con.close()

def get_all_reservations():
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    print("Reservation: ID, Total price, Time of reservation, User ID, Show ID")
    for row in cur.execute("SELECT * FROM reservation"):
        print(row)
    con.close()

def get_all_halls():
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    print("Hall: ID, Name of Hall, Row, Seat, Total seats")
    for row in cur.execute("SELECT * FROM hall"):
        print(row)
    con.close()

def get_all_shows():
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    print("Show: ID, Movie ID, Hall ID, Showtime")
    for row in cur.execute("SELECT * FROM shows"):
        print(row)
    con.close()

def get_all_seats():
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    print("Seat: ID, Status, Row, Seat, Price, Reservation ID, Show ID")
    for row in cur.execute("SELECT * FROM seat"):
        print(row)
    con.close()

def get_seats_for_show(show_id):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        seats = cur.execute("""SELECT id, status, row_number, seat_number, price, reservation_id FROM seat WHERE show_id = ? """, (show_id,)).fetchall()
        print(f"Fetching seats for show_id={show_id}")
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
    print("Logs/History: ID, Action, Timestamp of action, User ID, Reservation ID")
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
    cur.execute("SELECT * FROM movies WHERE id = ?", (id,))
    result = cur.fetchall()
    con.close()
    if result:
        return result
    else:
        return None

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

def get_movie_runtime(id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT runtime FROM movie WHERE id = ?", (id,))
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

def get_movie_category(id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    cur.execute("SELECT category FROM movies WHERE id = ?", (id,))
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

def get_reservations_for_user(user_id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM reservation WHERE user_id = ?", (user_id,)):
        print(row)
    con.close()


# genres as String-list are input,
# for example: filter_movies_by_genre("Action, Drama")
# filters only now_playing movies
def filter_movies_by_genres(genres):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()

    # Split input genres by ',' and remove leading whitespaces
    genre_list = []
    for genre in genres.split(","):
        genre_list.append(genre.strip())

    # Build the WHERE clause dynamically to check for all genres
    conditions_list = []
    for genre in genre_list:
        conditions_list.append("genres LIKE ?")
    conditions = " AND ".join(conditions_list)

    # SQL query with dynamic conditions
    query = f"SELECT * FROM movies WHERE category = 'now_playing' AND {conditions}"

    # Add wildcards for each genre for partial matching
    parameters = []
    for genre in genre_list:
        parameters.append(f"%{genre}%")

    # Execute query
    cur.execute(query, parameters)

    # Print results
    rows = cur.fetchall()
    for row in rows:
        print(row)

    con.close()


def filter_movies_by_vote_average(vote_average):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()

    query = "SELECT * FROM movies WHERE category = 'now_playing'"

    if vote_average == "> 9":
        query = "SELECT * FROM movies WHERE category = 'now_playing' AND vote_average > 9"
    if vote_average == "> 8":
        query = "SELECT * FROM movies WHERE category = 'now_playing' AND vote_average > 8"
    if vote_average == "> 7":
        query = "SELECT * FROM movies WHERE category = 'now_playing' AND vote_average > 7"
    if vote_average == "> 6":
        query = "SELECT * FROM movies WHERE category = 'now_playing' AND vote_average > 6"
    if vote_average == "> 5":
        query = "SELECT * FROM movies WHERE category = 'now_playing' AND vote_average > 5"

    cur.execute(query)

    rows = cur.fetchall()
    for row in rows:
        print(row)

    con.close()

def filter_movies_by_duration(duration):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()

    query = "SELECT * FROM movies WHERE category = 'now_playing'"

    if duration == "Less than 90 minutes":
        query = "SELECT * FROM movies WHERE category = 'now_playing' AND runtime < 90"
    if duration == "90-120 minutes":
        query = "SELECT * FROM movies WHERE category = 'now_playing' AND runtime BETWEEN 90 AND 120"
    if duration == "More than 120 minutes":
        query = "SELECT * FROM movies WHERE category = 'now_playing' AND runtime > 120"

    cur.execute(query)

    rows = cur.fetchall()
    for row in rows:
        print(row)

    con.close()

def filter_movies_by_keywords(keywords):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()

    keyword_list = []
    for keyword in keywords.split():
        keyword_list.append(keyword.strip())

    conditions_list = []
    for keyword in keyword_list:
        conditions_list.append("(LOWER(title) LIKE ? OR LOWER(overview) LIKE ?)")
    conditions = " AND ".join(conditions_list)

    query = f"SELECT * FROM movies WHERE category = 'now_playing' AND {conditions}"

    parameters = []
    for keyword in keyword_list:
        parameters.append(f"%{keyword.lower()}%")
        parameters.append(f"%{keyword.lower()}%")

    cur.execute(query, parameters)
    rows = cur.fetchall()
    for row in rows:
        print(row)

    con.close()

# example for function call
# filter_movies(genres="Animation", keywords=" mufasa king", vote_average="> 7", duration="90-120 minutes")
def filter_movies(genres=None, vote_average=None, duration=None, keywords=None):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()

    conditions_list = []
    parameters = []

    # Genre Filter
    if genres:
        genre_list = []
        for genre in genres.split(","):
            genre_list.append(genre.strip())
        for genre in genre_list:
            conditions_list.append("genres LIKE ?")
            parameters.append(f"%{genre}%")

    # Vote Average Filter
    if vote_average:
        if vote_average == "> 9":
            conditions_list.append("vote_average > 9")
        elif vote_average == "> 8":
            conditions_list.append("vote_average > 8")
        elif vote_average == "> 7":
            conditions_list.append("vote_average > 7")
        elif vote_average == "> 6":
            conditions_list.append("vote_average > 6")
        elif vote_average == "> 5":
            conditions_list.append("vote_average > 5")

    # Duration Filter
    if duration:
        if duration == "Less than 90 minutes":
            conditions_list.append("runtime < 90")
        elif duration == "90-120 minutes":
            conditions_list.append("runtime BETWEEN 90 AND 120")
        elif duration == "More than 120 minutes":
            conditions_list.append("runtime > 120")

    # Keyword Filter
    if keywords:
        keyword_list = []
        for keyword in keywords.split():
            keyword_list.append(keyword.strip())
        for keyword in keyword_list:
            conditions_list.append("(LOWER(title) LIKE ? OR LOWER(overview) LIKE ?)")
            parameters.extend([f"%{keyword.lower()}%", f"%{keyword.lower()}%"])

    # Combine all conditions
    conditions = " AND ".join(conditions_list)
    query = f"SELECT * FROM movies WHERE category = 'now_playing'"
    if conditions:
        query += f" AND {conditions}"

    # Execute the query
    cur.execute(query, parameters)
    rows = cur.fetchall()
    for row in rows:
        print(row)

    con.close()
    return rows

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

def update_seat_status(seat_id, new_status, reservation_id = None):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        if reservation_id is None:
            cur.execute("UPDATE seat SET status = ? WHERE id = ? AND reservation_id IS NULL", (new_status, seat_id))
            con.commit()
        else:
            cur.execute("UPDATE seat SET status = ? WHERE id = ? AND reservation_id = ?", (new_status, seat_id, reservation_id))
            con.commit()
        # rowcount is number of changed rows while updating
        if cur.rowcount > 0:
            print(f"Seat with ID {seat_id} in reservation {reservation_id} updated: status = {new_status}")
        else:
            print(f"No seat found with ID {seat_id}.")
    except sqlite3.Error as e:
        print(f"Error while updating seat status: {e}")
    finally:
        con.close()

def update_seat_reservation_id_and_status(seat_id, reservations_id):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("UPDATE seat SET reservation_id = ? WHERE id = ?", (reservation_id, seat_id))
        con.commit()
        if cur.rowcount > 0:
            print(f"Seat with ID {seat_id} updated: reservation id = {reservation_id}")
        else:
            print(f"No seat found with ID {seat_id} or reservation ID {reservation_id}")

        cur.execute("UPDATE seat SET status = 'booked' WHERE id = ?", (seat_id,))
        con.commit()
        if cur.rowcount > 0:
            print(f"Seat with ID {seat_id} updated: status = booked")
        else:
            print(f"No seat found with ID {seat_id}")

    except sqlite3.Error as e:
        print(f"Error while updating reservation id of seat: {e}")
    finally:
        con.close()
def calculate_total_price(seat_ids, show_id):
    if not seat_ids: # if no seats selected
        return 0.0

    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()

        # get prices of selected seats
        placeholders = ", ".join(["?"] * len(seat_ids))
        query = f"""
            SELECT SUM(price)
            FROM seat
            WHERE id IN ({placeholders}) AND show_id = ?
        """
        cur.execute(query, (*seat_ids, show_id))
        total_price = cur.fetchone()[0]

        con.close()
        if total_price is not None:
            return total_price
        else:
            return 0.0
    except Exception as e:
        print(f"Error while calculating total_price: {e}")
        return 0.0

# Functions for statistic analysis
def check_for_admin(user_id):
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("SELECT role FROM user WHERE id = ?", (user_id,))
        result = cur.fetchone()
        if result:
            if result[0] == "Admin":
                return 1
            else:
                return 0
        else:
            return None
    except sqlite3.Error as e:
        print(f"Error while calculating total price: {e}")
    finally:
        con.close()

# Input parameter: list of seat id's
def is_seat_available(seats):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    result = True
    for seat in seats:
        cur.execute("SELECT reservation_id FROM seat WHERE id = ?", (seat,))
        res = cur.fetchone()
        if res[0] is not None:
            result = False
    con.close()
    return result

def calculate_number_available_seats(show_id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM seat WHERE show_id = ? AND status = 'free'", (show_id,))
    result = cur.fetchone()

    con.close()
    if result:
        return result[0]
    else:
        return None

def calculate_number_not_available_seats(show_id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM seat WHERE show_id = ? AND status = 'booked' OR status = 'selected'", (show_id,))
    result = cur.fetchone()

    con.close()
    if result:
        return result[0]
    else:
        return None

def calculate_percentage_available_seats(show_id):
    available = calculate_number_available_seats(show_id)
    percentage = available/200
    percentage = (float)(percentage * 100)
    return percentage

def calculate_percentage_not_available_seats(show_id):
    available = calculate_number_not_available_seats(show_id)
    percentage = available/200
    percentage = (float)(percentage * 100)
    return percentage

def list_of_available_seats(show_id):
    con = sqlite3.connect("movies.db")
    cur = con.cursor()

    list_available_seats = []
    cur.execute("SELECT * FROM seat WHERE show_id = ? AND status = 'free'", (show_id,))
    result = cur.fetchall()
    for r in result:
        list_available_seats.append(r)
    con.close()
    return list_available_seats

def list_of_not_available_seats():
    con = sqlite3.connect("movies.db")
    cur = con.cursor()

    list_not_available_seats = []
    cur.execute("SELECT * FROM seat WHERE show_id = ? AND status != 'free'", (show_id,))
    result = cur.fetchall()
    for r in result:
        list_not_available_seats.append(r)
    con.close()
    return list_not_available_seats

# except for their password
def number_of_users_with_information():
    con = sqlite3.connect("movies.db")
    cur = con.cursor()

    user_number = 0
    cur.execute("SELECT COUNT(*) FROM user")
    result = cur.fetchone()
    if result:
        user_number = result[0]

    cur.execute("SELECT id, vorname, nachname, email, role FROM user")
    result = cur.fetchall()
    if result:
        print(f"Number of current users: {user_number}")
        print("")
        for row in result:
            print(row)
    else:
        print(f"Number of current users: {user_number}")

def pie_chart_seats(show_id):
    labels = ['Available', 'Not Available']
    sizes1 = [calculate_number_available_seats(show_id), calculate_number_not_available_seats(show_id)]
    sizes2 = [calculate_percentage_available_seats(show_id), calculate_percentage_not_available_seats(show_id)]

    # Set up the figure size and layout
    fig, axs = plt.subplots(2, 1, figsize=(8, 12), constrained_layout=True)

    # Colors and styles
    colors = ['#4CAF50', '#E57373']

    # First pie chart
    axs[0].set_title("Total Seats: Available vs. Not Available", fontsize=16, fontweight='bold')
    axs[0].pie(sizes1, labels=labels, colors=colors, autopct=lambda p: f'{int(round(p/100*sum(sizes1)))}', shadow=True, startangle=90,
               wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})

    # Second pie chart
    axs[1].set_title("Percentage: Available vs. Not Available", fontsize=16, fontweight='bold')
    axs[1].pie(sizes2, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90,
               wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})

    # Save the figure with higher DPI for better quality
    plt.savefig("pie_chart_seats.png", dpi=300)
