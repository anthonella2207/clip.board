# ***************************************************************************************
# DESCRIPTION

# Here you can find all the functions to call our database.

# We have all the functions for ...

# a) Adding data
# b) Getting data
# c) Deleting data
# d) Setting/Updating data

# ***************************************************************************************

# Imports
import sqlite3 # Documentation: https://docs.python.org/3/library/sqlite3.html
import requests
import json

# Connecting with our database
con = sqlite3.connect("cinema.db")
cur = con.cursor()

# a) Adding data
def add_movie(iD, year, genre, movie_name, duration, regisseur, bewertung):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO movie VALUES
                (?, ?, ?, ?, ?, ?, ?)
        """, (iD, year, genre, movie_name, duration, regisseur, bewertung))
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
        con = sqlite3.connect("cinema.db")
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

def add_showtime(iD, date, time):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO showtime VALUES
                (?, ?, ?)
        """, (iD, date, time))
        con.commit()
        print(f"Showtime {iD} added.")
    except sqlite3.IntegrityError:
        print(f"Error while adding user: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

def add_reservation(iD, total_price, time_of_reservation, user_iD, showtime_iD):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO reservation VALUES
                (?, ?, ?, ?, ?)
        """, (iD, total_price, time_of_reservation, user_iD, showtime_iD))
        con.commit()
        print(f"Reservation {iD} added.")
    except sqlite3.IntegrityError:
        print(f"Error while adding user: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

def add_hall(iD, hall_name, row_count, seats_per_row, total_seats):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO hall VALUES
                (?, ?, ?, ?, ?)
        """, (iD, hall_name, row_count, seats_per_row, total_seats))
        con.commit()
        print(f"Hall {hall_name} added.")
    except sqlite3.IntegrityError:
        print(f"Error while adding user: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

def add_seat(iD, status, row_number, seat_number, price, reservation_iD, hall_iD):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO seat VALUES
                (?, ?, ?, ?, ?, ?, ?)
        """, (iD, status, row_number, seat_number, price, reservation_iD, hall_iD))
        con.commit()
        print(f"Seat {iD} added.")
    except sqlite3.IntegrityError:
        print(f"Error while adding user: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

def add_showtime_includes_movie(movie_iD, showtime_iD):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO showtime_includes_movie VALUES
                (?, ?)
        """, (movie_iD, showtime_iD))
        con.commit()
        print(f"Showtime includes movie ({movie_iD}, {showtime_iD}) added.")
    except sqlite3.IntegrityError:
        print(f"Error while adding user: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

def add_movie_in_hall(movie_iD, hall_iD):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO showtime_includes_movie VALUES
                (?, ?)
        """, (movie_iD, hall_iD))
        con.commit()
        print(f"Movie in hall ({movie_iD}, {hall_iD}) added.")
    except sqlite3.IntegrityError:
        print(f"Error while adding user: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

def add_logs_history(iD, action, action_timestamp, user_iD, reservation_iD):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO logs_history VALUES
                (?, ?, ?, ?, ?)
        """, (iD, action, action_timestamp, user_iD, reservation_iD))
        con.commit()
        print(f"Logs and history {iD} added.")
    except sqlite3.IntegrityError:
        print(f"Error while adding user: IntegrityError")
    except:
        print("Error occured")
    finally:
        con.close()

# b) Getting data
def get_all_users():
    con = sqlite3.connect("cinema.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM user"):
        print(row)
    con.close()

def get_all_showtimes():
    con = sqlite3.connect("cinema.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM showtime"):
        print(row)
    con.close()

def get_all_reservations():
    con = sqlite3.connect("cinema.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM reservation"):
        print(row)
    con.close()

def get_all_halls():
    con = sqlite3.connect("cinema.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM hall"):
        print(row)
    con.close()

def get_all_seats():
    con = sqlite3.connect("cinema.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM seat"):
        print(row)
    con.close()

def get_all_movies():
    con = sqlite3.connect("cinema.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM movie"):
        print(row)
    con.close()

def get_all_logs_histories():
    con = sqlite3.connect("cinema.db")
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM logs_history"):
        print(row)
    con.close()

def get_movie_id(original_title):
    con = sqlite3.connect("cinema.db")
    cur = con.cursor()
    cur.execute("SELECT id FROM movie WHERE original_title = ?", (original_title,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    else:
        return None
def get_posterurl(movie_id):
    con = sqlite3.connect("cinema.db")
    cur = con.cursor()
    poster_baseURL = "https://image.tmdb.org/t/p/w500"
    cur.execute("SELECT poster_path FROM movie WHERE id = ?", (movie_id,))
    result = cur.fetchone()
    con.close()
    if result:
        print(poster_baseURL + str(result[0]))
    else:
        return None

# c) Deleting data
def delete_user(user_iD):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("DELETE FROM user WHERE id = ?", (user_iD,))
        con.commit()
        print(f"User with ID {user_iD} deleted.")
    except sqlite3.Error as e:
        print(f"Error while deleting movie: {e}")
    finally:
        con.close()

def delete_movie(movie_iD):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("DELETE FROM movie WHERE ID = ?", (movie_iD,))
        con.commit()
        print(f"Movie with ID {movie_iD} deleted.")
    except sqlite3.Error as e:
        print(f"Error while deleting movie: {e}")
    finally:
        con.close()

def delete_showtime(showtime_iD):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("DELETE FROM showtime WHERE id = ?", (showtime_iD,))
        con.commit()
        print(f"Showtime with ID {showtime_iD} deleted.")
    except sqlite3.Error as e:
        print(f"Error while deleting movie: {e}")
    finally:
        con.close()

def delete_reservation(reservation_iD):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("DELETE FROM reservation WHERE id = ?", (reservation_iD,))
        con.commit()
        print(f"Reservation with ID {reservation_iD} deleted.")
    except sqlite3.Error as e:
        print(f"Error while deleting movie: {e}")
    finally:
        con.close()

def delete_hall(hall_iD):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("DELETE FROM hall WHERE id = ?", (hall_iD,))
        con.commit()
        print(f"Hall with ID {hall_iD} deleted.")
    except sqlite3.Error as e:
        print(f"Error while deleting movie: {e}")
    finally:
        con.close()

def delete_seat(seat_iD):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("DELETE FROM seat WHERE id = ?", (seat_iD,))
        con.commit()
        print(f"Seat with ID {seat_iD} deleted.")
    except sqlite3.Error as e:
        print(f"Error while deleting movie: {e}")
    finally:
        con.close()

def delete_logs_history(logs_history_iD):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("DELETE FROM logs_history WHERE id = ?", (logs_history_iD,))
        con.commit()
        print(f"Log/history with ID {logs_history_iD} deleted.")
    except sqlite3.Error as e:
        print(f"Error while deleting movie: {e}")
    finally:
        con.close()

# d) Setting/Updating data
def update_seat_status(seat_iD, new_status):
    try:
        con = sqlite3.connect("cinema.db")
        cur = con.cursor()
        cur.execute("UPDATE seat SET status = ? WHERE id = ?", (new_status, seat_iD))
        con.commit()
        # rowcount is number of changed rows while updating
        if cur.rowcount > 0:
            print(f"Seat with ID {seat_iD} updated: status = {new_status}")
        else:
            print(f"No seat found with ID {seat_iD}.")
    except sqlite3.Error as e:
        print(f"Error while updating seat status: {e}")
    finally:
        con.close()
