import sqlite3

# Verbindung zur DB
con = sqlite3.connect('movies.db')
cur = con.cursor()

# Teste die Abfrage direkt
email = 'emilysophie.aust@stud.uni-goettingen.de'
cur.execute("SELECT * FROM user WHERE email = ?", (email,))
user = cur.fetchone()

print(user)
con.close()