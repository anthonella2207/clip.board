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
# d) Updating data
# e) Statistics


# TABLE OF FUNCTIONS

# a) Adding data
# line: 106; add_movie(iD, year, genre, movie_name, duration, regisseur, bewertung)
# line: 127; add_user(iD, vorname, nachname, password, email, role)
# line: 151; add_show(id, movie_id, hall_id, showtime)
# line: 171; add_reservation(id, total_price, time_of_reservation, user_id, show_id)
# line: 210; add_hall(iD, hall_name, row_count, seats_per_row, total_seats)
# line: 230; add_seat(id, status, row_number, seat_number, price, reservation_id, show_iD)
# line: 250; add_logs_history(iD, action, action_timestamp, user_iD, reservation_iD)

# b) getting data
# line: 271; get_all_users()
# line: 282; get_all_reservations()
# line: 293; get_all_halls()
# line: 304; get_all_shows()
# line: 315; get_all_seats()
# line: 326; get_seats_for_show(show_id)
# line: 355; get_all_movies()
# line: 366; get_all_now_playing_movies()
# line: 378; get_all_logs_histories()
# line: 389; login_check_for_user(email)
# line: 404: login_check_password(email, password)
# line: 422; get_movie_id(title)
# line: 435; get_movie(id)
# line: 449; get_movie_adult(id)
# line: 464; get_movie_runtime(id)
# line: 479; get_movie_genre(id)
# line: 494; get_movie_title(id)
# line: 508; get_movie_overview(id)
# line: 522; get_movie_release_date(id)
# line: 537; get_movie_vote_average(id)
# line: 552; get_movie_category(id)
# line: 567; get_posterurl(movie_id)
# line: 583; get_user_id(email)
# line: 598; get_user_vorname(id)
# line: 613; get_user_nachname(id)
# line: 628; get_user_email(id)
# line: 643; get_user_role(id)
# line: 658; get_reservations_for_user(user_id)
# line: 673; filter_movies_by_genres(genres)
# line: 713; filter_movies_by_vote_average(vote_average)
# line: 742; filter_movies_by_duration(duration)
# line: 767; filter_movies_by_keywords(keywords)
# line: 802; filter_movies(genres=None, vote_average=None, duration=None, keywords=None)

#c) deleting data
# line: 851; delete_user(user_iD)
# line: 866; delete_movie(movie_iD)
# line: 881; delete_reservation(reservation_iD)
# line: 896; delete_hall(hall_iD)
# line: 911; delete_seat(seat_iD)
# line: 926; delete_logs_history(logs_history_iD)

#d) setting/updating data
# line: 943; update_user_name(user_id, new_vorname, new_nachname)
# line: 964; update_user_email(user_id, new_email)
# line: 984; update_user_password(user_id, new_password)
# line: 1005; update_user_role(user_id, new_role)
# line: 1024; update_seat_status(seat_id, new_status, reservation_id = None)
# line: 1050; update_seat_reservation_id_and_status(seat_id, reservation_id)
# line: 1081; calculate_total_price(seat_ids, show_id)
# line: 1114; check_for_admin(user_id)
# line: 1137; is_seat_available(seats)
# line: 1156; calculate_number_available_seats(show_id)
# line: 1173; calculate_number_not_available_seats(show_id)
# line: 1190; calculate_percentage_available_seats(show_id)
# line: 1200; calculate_percentage_not_available_seats(show_id)
# line: 1210; list_of_available_seats(show_id)
# line: 1226; list_of_not_available_seats()
# line: 1243; number_of_users_with_information()
# line: 1267; pie_chart_seats(show_id)

# ***************************************************************************************

# Imports
import sqlite3 # Documentation: https://docs.python.org/3/library/sqlite3.html
import requests
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime
from sqlalchemy import except_

# Connecting with our database
con = sqlite3.connect("movies.db")
cur = con.cursor()

# a) Adding data
def add_movie(id, title, release_date, overview, vote_average, poster_path, category, genres, runtime, adult):
    """
    Description: This function adds a movie into the database movies.db.
    """
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
    """
    Description: This function adds a user into the database movies.db.
    """
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO user VALUES
                (?, ?, ?, ?, ?, ?)
        """, (iD, vorname, nachname, password, email, role))
        con.commit()
        print(f"User {vorname} {nachname} added.")

        #add_logs_history(None, "User Added", datetime.now(), None, None)
        con.commit()

    except sqlite3.IntegrityError:
        print(f"Error while adding user: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

def add_show(id, movie_id, hall_id, showtime):
    """
    Description: This function adds a show into the database movies.db.
    """
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
    """
    Description: This function adds a reservation into the database movies.db.
    """
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()

        cur.execute("""
            INSERT INTO reservation(id, total_price, time_of_reservation, user_id, show_id)
            VALUES (NULL, ?, ?, ?, ?)
        """, (total_price, time_of_reservation, user_id, show_id))
        con.commit()

        #  Sicherstellen, dass reservation_id korrekt gesetzt ist
        reservation_id = cur.lastrowid
        print(f"reservierung erfolgreich: ID {reservation_id}")

        if reservation_id is None:
            print("Fehler: reservation_id ist None!")
            return None

        #add_logs_history(None, "Seat reservation", datetime.now(), user_id, reservation_id)
        con.commit()

        return reservation_id

    except sqlite3.IntegrityError as e:
        print(f"Datenbankfehler (IntegrityError): {e}")
        return None
    except sqlite3.Error as e:
        print(f"SQLite-Fehler: {e}")
        return None
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")
        return None
    finally:
        con.close()

def add_hall(iD, hall_name, row_count, seats_per_row, total_seats):
    """
    Description: This function adds a hall into the database movies.db.
    """
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
    """
    Description: This function adds a seat into the database movies.db.
    """
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

def add_logs_history(action, user_iD, reservation_iD = None):
    """
    Description: This function adds logs and histories into the database movies.db.
    """
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO logs_history (action, action_timestamp, user_id, reservation_id)
            VALUES (?, datetime('now'), ?, ?)
        """, (action, user_iD, reservation_iD))
        con.commit()
        print(f"Logs-history added: {action}, User: {user_iD}, Reservation: {reservation_iD}")
    except sqlite3.IntegrityError:
        print(f"Error while adding Logs/History: IntegrityError")
    except Exception as e:
        print("Error occured")
    finally:
        con.close()

# b) Getting data
def get_all_users():
    """
    Description: This function gets and prints all users from the database movies.db.
    """
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    print("User: ID, First Name, Last Name, Password, E-Mail, Role")
    for row in cur.execute("SELECT * FROM user"):
        print(row)
    con.close()

def get_all_reservations():
    """
    Description: This function gets and prints all reservations from the database movies.db.
    """
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    print("Reservation: ID, Total price, Time of reservation, User ID, Show ID")
    for row in cur.execute("SELECT * FROM reservation"):
        print(row)
    con.close()

def get_all_halls():
    """
    Description: This function gets and prints all halls from the database movies.db.
    """
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    print("Hall: ID, Name of Hall, Row, Seat, Total seats")
    for row in cur.execute("SELECT * FROM hall"):
        print(row)
    con.close()

def get_all_shows():
    """
    Description: This function gets and prints all shows from the database movies.db.
    """
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    print("Show: ID, Movie ID, Hall ID, Showtime")
    for row in cur.execute("SELECT * FROM shows"):
        print(row)
    con.close()

def get_all_seats():
    """
    Description: This function gets and prints all seats from the database movies.db.
    """
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    print("Seat: ID, Status, Row, Seat, Price, Reservation ID, Show ID")
    for row in cur.execute("SELECT * FROM seat"):
        print(row)
    con.close()

def get_seats_for_show(show_id):
    """
    Description: This function gets and prints all seats with attributes ID, status, row number, seat number,
    price and reservation ID where the show ID equals the given show ID from the database movies.db.
    """
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
    """
    Description: This function gets and prints all movies from the database movies.db.
    """
    con = sqlite3.connect("movies.db")
    cur = con.cursor()

    for row in cur.execute("SELECT * FROM movies"):
        print(row)
    con.close()

def get_all_now_playing_movies():
    """
    Description: This function gets and prints all movies that are assigned to category 'now_playing'
    from the database movies.db.
    """
    con = sqlite3.connect("movies.db")
    cur = con.cursor()

    for row in cur.execute("SELECT * FROM movies WHERE category = ?", ('now_playing',)):
        print(row)
    con.close()

def get_all_logs_histories():
    """
    Description: This function gets and prints all logs and histories from the database movies.db.
    """
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    print("Logs/History: ID, Action, Timestamp of action, User ID, Reservation ID")
    for row in cur.execute("SELECT * FROM logs_history"):
        print(row)
    con.close()

def login_check_for_user(email):
    """
    Description: This function gets the user that has the given email adress
    from the database movies.db, if it exists.
    """
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
    """
    Description: This function checks if the given email adress and password are matching in the
    database movies.db.
    """
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
    """
    Description: This function gets the movie ID with the given title from the database movies.db.
    """
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
    """
    Description: This function gets the movie with the given ID from the database movies.db.
    """
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
    """
    Description: This function gets the adult attribute of a movie with given ID
    from the database movies.db.
    """
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
    """
    Description: This function gets the runtime of a movie with given ID
    from the database movies.db.
    """
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
    """
    Description: This function gets the genres of a movie with given ID
    from the database movies.db.
    """
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
    """
    Description: This function gets the title of a movie with given ID
    from the database movies.db.
    """
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
    """
    Description: This function gets the overview of a movie with given ID
    from the database movies.db.
    """
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
    """
    Description: This function gets the release date of a movie with given ID
    from the database movies.db.
    """
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
    """
    Description: This function gets the vote average of a movie with given ID
    from the database movies.db.
    """
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
    """
    Description: This function gets the category of a movie with given ID
    from the database movies.db.
    """
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
    """
    Description: This function gets the poster URL of a movie with given ID
    from the database movies.db.
    """
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
    """
    Description: This function gets the ID of a user with given email
    from the database movies.db.
    """
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
    """
    Description: This function gets the first name of a user with given ID
    from the database movies.db.
    """
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
    """
    Description: This function gets the last name of a user with given ID
    from the database movies.db.
    """
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
    """
    Description: This function gets the email adress of a user with given ID
    from the database movies.db.
    """
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
    """
    Description: This function gets the role of a user with given ID
    from the database movies.db.
    """
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
    """
    Description: This function gets the reservations of a user with given ID
    from the database movies.db.
    """
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM reservation WHERE user_id = ?", (user_id,)):
        print(row)
    con.close()


# genres as String-list are input,
# for example: filter_movies_by_genre("Action, Drama")
# filters only now_playing movies
def filter_movies_by_genres(genres):
    """
    Description: This functions filters and prints now playing movies from the database movies.db by genres.
    Parameters: list of strings.
    """
    con = sqlite3.connect("movies.db")
    cur = con.cursor()

    # Split input genres by ',' and remove leading whitespaces
    genre_list = []
    for genre in genres.split(","):
        genre_list.append(genre.strip())

    # Build the WHERE clause dynamically to check for all genres
    conditions_list = []
    for genre in genre_list:
        conditions_list.append("genres LIKE '%' || ? || '%'")

    conditions = " AND ".join(conditions_list)

    # SQL query with dynamic conditions
    query = f"SELECT * FROM movies WHERE category = 'now_playing' AND {conditions}"

    # Add wildcards for each genre for partial matching
    parameters = []
    for genre in genre_list:
        conditions_list.append("genres LIKE '%' || ? || '%'")
        parameters.append(genre)

    # Execute query
    cur.execute(query, parameters)

    # Print results
    rows = cur.fetchall()
    for row in rows:
        print(row)

    con.close()


def filter_movies_by_vote_average(vote_average):
    """
    Description: This functions filters and prints now playing movies from the database movies.db by their vote average.
    Parameters: string.
    """
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
    """
    Description: This functions filters and prints now playing movies from the database movies.db by their duration.
    Parameters: string.
    """
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
    """
    Description: This functions filters and prints now playing movies from the database movies.db by keywords.
                 Title and overview of movies get filtered. If more than one keyword is input, all
                 keywords have to be in title or overview, not just one of them.
    Parameters: string.
    """
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
def filter_movies(genres=None, duration=None, keywords=None, vote_average=None):
    """
    Description: This functions filters now playing movies from the database movies.db by their genres, duration,
                 keywords and vote average.
    Parameters:  genres as list of strings, duration as string, keywords as string, vote average as string.
                 All have None as default.
    """
    con = sqlite3.connect("movies.db")
    cur = con.cursor()

    conditions_list = ["category = 'now_playing'"]  # Nur Now-Playing-Filme
    parameters = []

    # Genre-Filter: Prüfen, ob das Genre in der Liste enthalten ist
    if genres and genres != "All":
        conditions_list.append("genres LIKE '%' || ? || '%'")
        parameters.append(genres)

    # Dauer-Filter
    if duration and duration != "All":
        if duration == "<90":
            conditions_list.append("runtime < 90")
        elif duration == "90-120":
            conditions_list.append("runtime BETWEEN 90 AND 120")
        elif duration == ">120":
            conditions_list.append("runtime > 120")

    #vote_average
    if vote_average is not None:  # Stelle sicher, dass `vote_average` verarbeitet wird!
        conditions_list.append("vote_average > ?")
        parameters.append(vote_average)

    # Keywords in Titel oder Beschreibung suchen
    if keywords:
        keyword_list = keywords.split()
        for keyword in keyword_list:
            conditions_list.append("(LOWER(title) LIKE ? OR LOWER(overview) LIKE ?)")
            parameters.extend([f"%{keyword.lower()}%", f"%{keyword.lower()}%"])

    # Kombiniere alle Bedingungen
    conditions = " AND ".join(conditions_list)
    query = f"SELECT * FROM movies WHERE {conditions}"

    cur.execute(query, parameters)
    rows = cur.fetchall()
    con.close()
    return rows

# c) Deleting data
def delete_user(user_iD):
    """
    Description: This function deletes a user with given ID from the database movies.db.
    """
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
    """
    Description: This function deletes a movie with given ID from the database movies.db.
    """
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
    """
    Description: This function deletes reservation with given ID from the database movies.db.
    """
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
    """
    Description: This function deletes a hall with given ID from the database movies.db.
    """
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
    """
    Description: This function deletes a seat with given ID from the database movies.db.
    """
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
    """
    Description: This function deletes a log or history with given ID from the database movies.db.
    """
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
    """
    Description: This function updates the user's first and last name with given ID in the database movies.db.
    Parameters: user ID as int, new first name as string, new last name as string.
    """
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
    """
    Description: This function updates the user's email adress with given ID in the database movies.db.
    Parameters: user ID as int, new email adress as string.
    """
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

def update_user_password(user_id, new_password):
    """
    Description: This function updates the user's password with given ID in the database movies.db.
    Parameters: user ID as int, new password as string.
    """
    try:
        con = sqlite3.connect("movies.db")
        cur = con.cursor()
        cur.execute("UPDATE user SET password = ? WHERE id = ?", (new_password, user_id))
        con.commit()
        if cur.rowcount > 0:
            print("User with ID {user_id} updated: password = {new_password}")
        else:
            print(f"No user found with ID {user_id}.")

    except sqlite3.Error as e:
        print(f"Error while updating users password: {e}")
    finally:
        con.close()

# Hint: only Admins can change user roles!
def update_user_role(user_id, new_role):
    """
    Description: This function updates the user's role with given ID in the database movies.db.
    Parameters: user ID as int, new role as string.
    """
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
    """
    Description: This function updates the seat status with given ID in the database movies.db.
                 There is an option to change the reservation ID as well.
    Parameters:  seat ID as int, new status as string, reservation ID as int (None is default).
    """
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

def update_seat_reservation_id_and_status(seat_id, reservation_id):
    """
    Description: This function updates the seat status with given ID and it's assigned reservation ID
                 in the database movies.db.
    Parameters:  seat ID as int, reservation ID as int.
    """
    try:
        if reservation_id is None:
            return

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
    """
    Description: This function calculates the total price of selected seats from the database movies.db
                 where the seats have a given show ID.
    Parameters:  list of seat ID's as int, show ID as int
    """
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
    """
    Description: This function checks if a user from the database movies.db with a given ID
                 has 'Admin' as his role.
    """
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
    """
    Description: This function checks if one or multiple seats from the database movies.db
                 are available and not booked yet.
    Parameters:  list of seats as int
    """
    con = sqlite3.connect("movies.db")
    cur = con.cursor()
    result = True
    for seat in seats:
        cur.execute("SELECT reservation_id FROM seat WHERE id = ?", (seat,))
        res = cur.fetchone()
        if res and res[0] is not None:
            result = False
            break
    con.close()
    return result

def calculate_number_available_seats(show_id):
    """
    Description: This function calculates the number of available seats for a show with given ID
                 in the database movies.db.
    """
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
    """
    Description: This function calculates the number of not available seats for a show with given ID
                 in the database movies.db.
    """
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
    """
    Description: This function calculates the percentage of available seats for a show with given ID
                 in the database movies.db.
    """
    available = calculate_number_available_seats(show_id)
    percentage = available/200
    percentage = (float)(percentage * 100)
    return percentage

def calculate_percentage_not_available_seats(show_id):
    """
    Description: This function calculates the percentage of not available seats for a show with given ID
                 in the database movies.db.
    """
    available = calculate_number_not_available_seats(show_id)
    percentage = available/200
    percentage = (float)(percentage * 100)
    return percentage

def list_of_available_seats(show_id):
    """
    Description: This function returns a list of available seats for a show with given ID
                 in the database movies.db.
    """
    con = sqlite3.connect("movies.db")
    cur = con.cursor()

    list_available_seats = []
    cur.execute("SELECT * FROM seat WHERE show_id = ? AND status = 'free'", (show_id,))
    result = cur.fetchall()
    for r in result:
        list_available_seats.append(r)
    con.close()
    return list_available_seats

def list_of_not_available_seats(show_id):
    """
    Description: This function returns a list of not available seats for a show with given ID
                 in the database movies.db.
    """
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
    """
    Description: This function calculates and prints the number of users with their information
                 from the database movies.db.
    """
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
    """
    Description: This function calculates statistics for a show with a given ID from the database movies.db
                    and generates pie charts for analysis. It calls to other functions to calculate the
                    number and percentage of available and not available seats.  MatplotLib is used for
                    printing pie charts. The results are saved in a .png format.
    """
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
