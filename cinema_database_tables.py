import sqlite3 # Documentation: https://docs.python.org/3/library/sqlite3.html

# create a new database and open database connection to allow sqlite3 to work with it
con = sqlite3.connect("cinema.db")

# create cursor to execute SQL statements and fetch results from SQL queries
cur = con.cursor()

# create database tables
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

cur.execute("""
CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username VARCHAR(20) NOT NULL UNIQUE,
	password VARCHAR(30) NOT NULL,
	email VARCHAR(30) NOT NULL UNIQUE,
	role VARCHAR(10) NOT NULL
);
""")

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

cur.execute("""
CREATE TABLE hall (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(20) NOT NULL,
	row_count INT NOT NULL,
	seats_per_row INT NOT NULL,
	total_seats INT NOT NULL
);
""")

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

cur.execute("""
CREATE TABLE showtime_includes_movie (
	movie_id INT,
	showtime_id INT,
	PRIMARY KEY (movie_id, showtime_id),
	FOREIGN KEY (movie_id) REFERENCES movie(id),
	FOREIGN KEY (showtime_id) REFERENCES showtime(id)
);
""")

cur.execute("""
CREATE TABLE movie_in_hall (
	movie_id INT,
	hall_id INT,
	PRIMARY KEY (movie_id, hall_id),
	FOREIGN KEY (movie_id) REFERENCES movie(id),
	FOREIGN KEY (hall_id) REFERENCES hall(id)
);
""")

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
