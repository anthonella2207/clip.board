import sqlite3 # Documentation: https://docs.python.org/3/library/sqlite3.html
import requests
import json
from cinema_functions_for_database import *

# create a new database and open database connection to allow sqlite3 to work with it
con = sqlite3.connect("cinema.db")

# create cursor to execute SQL statements and fetch results from SQL queries
cur = con.cursor()

# create database tables
cur.execute("DROP TABLE IF EXISTS movie;")
cur.execute("""
CREATE TABLE movie (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    poster_path VARCHAR(100) NOT NULL,
	adult INTEGER NOT NULL,
    genre VARCHAR(50) NOT NULL,
    origin_country VARCHAR(50) NOT NULL,
    origin_language VARCHAR(50) NOT NULL,
    original_title VARCHAR (50) NOT NULL,
    overview VARCHAR (1000) NOT NULL,
    release_date DATE NOT NULL,
    runtime INTEGER NOT NULL,
    vote_average REAL NOT NULL
);
""")

cur.execute("DROP TABLE IF EXISTS user;")
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

cur.execute("DROP TABLE IF EXISTS showtime;")
cur.execute("""
CREATE TABLE showtime (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time VARCHAR(50) NOT NULL
);
""")

cur.execute("DROP TABLE IF EXISTS reservation;")
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

cur.execute("DROP TABLE IF EXISTS hall;")
cur.execute("""
CREATE TABLE hall (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(20) NOT NULL,
	row_count INT NOT NULL,
	seats_per_row INT NOT NULL,
	total_seats INT NOT NULL
);
""")

cur.execute("DROP TABLE IF EXISTS seat;")
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

cur.execute("DROP TABLE IF EXISTS showtime_includes_movie;")
cur.execute("""
CREATE TABLE showtime_includes_movie (
	movie_id INT,
	showtime_id INT,
	PRIMARY KEY (movie_id, showtime_id),
	FOREIGN KEY (movie_id) REFERENCES movie(id),
	FOREIGN KEY (showtime_id) REFERENCES showtime(id)
);
""")

cur.execute("DROP TABLE IF EXISTS movie_in_hall;")
cur.execute("""
CREATE TABLE movie_in_hall (
	movie_id INT,
	hall_id INT,
	PRIMARY KEY (movie_id, hall_id),
	FOREIGN KEY (movie_id) REFERENCES movie(id),
	FOREIGN KEY (hall_id) REFERENCES hall(id)
);
""")

cur.execute("DROP TABLE IF EXISTS logs_history;")
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
add_user(1, "Anthonella Alessandra", "Frutos Lara", "1234", "a.frutoslara@stud.uni-goettingen.de", "Admin")
con.commit()
add_user(2, "Emily Sophie", "Aust", "1234", "emilysophie.aust@stud.uni-goettingen.de ", "Client")
con.commit()
add_user(3, "Cordula", "Maier", "1234", "cordula.maier@stud.uni-goettingen.de", "Client")
con.commit()

# add halls
add_hall(1, "Kino 1", 10, 20, 200)
con.commit()
add_hall(2, "Kino 2", 10, 20, 200)
con.commit()
add_hall(3, "Kino 3", 10, 20, 200)
con.commit()
add_hall(4, "Kino 4", 10, 20, 200)
con.commit()
add_hall(5, "Kino 5", 10, 20, 200)
con.commit()
add_hall(6, "Kino 6", 10, 20, 200)
con.commit()
add_hall(7, "Kino 7", 10, 20, 200)
con.commit()
add_hall(8, "Kino 8", 10, 20, 200)
con.commit()
add_hall(9, "Kino 9", 10, 20, 200)
con.commit()
add_hall(10, "Kino 10", 10, 20, 200)
con.commit()

# Add showtimes
add_showtime(None, '16:00')
add_showtime(None, '20:00')

#add seats
id_counter = 1
for hall_id in range(1, 11):
    price = 8
    for row_number in range(1, 11):
        if (row_number >= 5):
            price = 5
        for seat_number in range(1, 21):
            add_seat(id_counter, "free", row_number, seat_number, price, None, hall_id)
            con.commit()
            id_counter += 1

# add movies

# API-Key und Basis-URL
api_key = "ba4b24646d1f0f2334b8672694cc1cd6"
search_url = "https://api.themoviedb.org/3/search/movie"
details_url = "https://api.themoviedb.org/3/movie/{movie_id}"

queries = ["Sonic+3", "Mufasa", "Wicked", "The Lord of the Rings: The War of the Rohirrim", "Werewolves", "Kraven the Hunter", "Your Fault", "Elevation", "Dirty Angels", "Solo Leveling+Reawakening", "The Substance", "Flow", "Nosferatu", "Absolution", "The Wild Robot", "Ferry+2", "Saturday Night's Main Event", "Heretic", "Squid Game: Fireplace", "Vergeltung mit Flügeln", "Den of Thieves 2", "Anora", "Nightbitch", "A real pain", "Azrael"]
# Nach einem Film suchen
for q in queries:
    search_query = q
    response = requests.get(search_url, params={
        "api_key": api_key,
        "language": "en-US",
        "query": search_query
    })

    if response.status_code == 200:
        search_results = response.json().get("results", [])
        if search_results:
            # Ersten Treffer auswählen (oder Benutzer entscheiden lassen)
            selected_movie = search_results[0]  # Beispiel: Erster Treffer
            movie_id = selected_movie["id"]

            # Zusätzliche Details abrufen
            details_response = requests.get(details_url.format(movie_id=movie_id), params={"api_key": api_key, "language": "en-US"})
            if details_response.status_code == 200:
                movie_details = details_response.json()

                # Film-Daten extrahieren
                movie = {
                    "id": movie_details["id"],
                    "poster_path": movie_details.get("poster_path", ""),
                    "adult": movie_details["adult"],
                    "genre": ", ".join([genre["name"] for genre in movie_details.get("genres", [])]),
                    "origin_country": ", ".join(movie_details.get("production_countries", [{}])[0].get("iso_3166_1", "")),
                    "origin_language": movie_details.get("original_language", ""),
                    "original_title": movie_details.get("original_title", ""),
                    "overview": movie_details.get("overview", ""),
                    "release_date": movie_details.get("release_date", ""),
                    "runtime": movie_details.get("runtime", 0),
                    "vote_average": movie_details.get("vote_average", 0.0)
                }

              # Film in die SQLite-Datenbank einfügen
                cur.execute("""
                INSERT INTO movie (id, poster_path, adult, genre, origin_country, origin_language, original_title, overview, release_date, runtime, vote_average)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    poster_path=excluded.poster_path,
                    adult=excluded.adult,
                    genre=excluded.genre,
                    origin_country=excluded.origin_country,
                    origin_language=excluded.origin_language,
                    original_title=excluded.original_title,
                    overview=excluded.overview,
                    release_date=excluded.release_date,
                    runtime=excluded.runtime,
                    vote_average=excluded.vote_average
                """, (
                    movie["id"],
                    movie["poster_path"],
                    movie["adult"],
                    movie["genre"],
                    movie["origin_country"],
                    movie["origin_language"],
                    movie["original_title"],
                    movie["overview"],
                    movie["release_date"],
                    movie["runtime"],
                    movie["vote_average"]
                ))
                con.commit()
                print(f"Film '{movie['original_title']}' erfolgreich hinzugefügt!")
            else:
                print(f"Fehler beim Abrufen der Filmdetails: {details_response.status_code}")
        else:
            print(f"Kein Film mit dem Titel '{search_query}' gefunden.")
    else:
        print(f"Fehler bei der Suche: {response.status_code}")

