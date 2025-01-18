import sqlite3 # Documentation: https://docs.python.org/3/library/sqlite3.html
import requests
import json
import cinema_functions_for_database

# create a new database and open database connection to allow sqlite3 to work with it
con = sqlite3.connect("cinema.db")

# create cursor to execute SQL statements and fetch results from SQL queries
cur = con.cursor()

# create database tables
cursor.execute("DROP TABLE IF EXISTS movie;")
cur.execute("""
CREATE TABLE movie (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	year INT NOT NULL,
	genre VARCHAR(30) NOT NULL,
	movie_name VARCHAR(50) NOT NULL,
	duration INT NOT NULL,
	regisseur VARCHAR(30) NOT NULL,
    bewertung FLOAT NOT NULL
);
""")

cursor.execute("DROP TABLE IF EXISTS user;")
cur.execute("""
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
cur.execute("""
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
cur.execute("""
CREATE TABLE hall (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(20) NOT NULL,
	row_count INT NOT NULL,
	seats_per_row INT NOT NULL,
	total_seats INT NOT NULL
);
""")

cursor.execute("DROP TABLE IF EXISTS seat;")
cur.execute("""
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
cur.execute("""
CREATE TABLE showtime_includes_movie (
	movie_id INT,
	showtime_id INT,
	PRIMARY KEY (movie_id, showtime_id),
	FOREIGN KEY (movie_id) REFERENCES movie(id),
	FOREIGN KEY (showtime_id) REFERENCES showtime(id)
);
""")

cursor.execute("DROP TABLE IF EXISTS movie_in_hall;")
cur.execute("""
CREATE TABLE movie_in_hall (
	movie_id INT,
	hall_id INT,
	PRIMARY KEY (movie_id, hall_id),
	FOREIGN KEY (movie_id) REFERENCES movie(id),
	FOREIGN KEY (hall_id) REFERENCES hall(id)
);
""")

cursor.execute("DROP TABLE IF EXISTS logs_history;")
cur.execute("""
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

# INITIAL VALUES

# insert some values
# using API to insert values in movie table

# add some users
add_user(1, "Anthonella Alessandra", "Frutos Lara", "1234", "a.frutoslara@stud.uni-goettingen.de ", "Admin")
add_user(2, "Emily Sophie", "Aust", "1234", "emilysophie.aust@stud.uni-goettingen.de ", "Client")
add_user(3, "Cordula", "Maier", "1234", "cordula.maier@stud.uni-goettingen.de", "Client")

# add halls
add_hall(1, "Kino 1", 10, 20, 200)
add_hall(2, "Kino 2", 10, 20, 200)
add_hall(3, "Kino 3", 10, 20, 200)
add_hall(4, "Kino 4", 10, 20, 200)
add_hall(5, "Kino 5", 10, 20, 200)
add_hall(6, "Kino 6", 10, 20, 200)
add_hall(7, "Kino 7", 10, 20, 200)
add_hall(8, "Kino 8", 10, 20, 200)
add_hall(9, "Kino 9", 10, 20, 200)
add_hall(10, "Kino 10", 10, 20, 200)

#add seats
for i in range(10):
    id_counter = 1
    price = 8
    for j in range(10):
        if (j >= 5):
            price = 5
        for k in range(20):
            add_seat(id_counter, "free", j, k, 8, None, i)
            id_counter+= 1


