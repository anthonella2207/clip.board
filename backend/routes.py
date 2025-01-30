from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, request, jsonify
import sqlite3
from flask_cors import cross_origin, CORS

#connection to our database
def get_db_connection():
    con = sqlite3.connect('movies.db')
    con.row_factory = sqlite3.Row
    print("Datenbank verbunden:", 'movies.db')  # Ausgabe zur Bestätigung
    return con

#Login routes
auth_routes = Blueprint('auth', __name__)
CORS(auth_routes)

@auth_routes.route('/login', methods=['POST'])
@cross_origin()
def login():
    try:
        data = request.get_json()
        print("Empfangene JSON-Daten:", data)
        if not data:
            return jsonify({"success": False, "message": "No JSON data received"}), 400

        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({"success": False, "message": "Missing email or password"}), 400

        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM user WHERE TRIM(email) = ?", (email.strip(),))
        user = cur.fetchone()
        con.close()

        if user:
            if user["password"] == password:
                return jsonify({"success": True, "message": "Login Successful", "role": user["role"]})
            else:
                return jsonify({"success": False, "message": "wrong password"}), 401
        else:
            return jsonify({"success": False, "message": "email not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": "Server error", "error": str(e)}), 500

#sign-up route

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
    con.close()

    return jsonify({"success": True, "message": "Registration successful"}), 201

seats_routes = Blueprint('seats_routes', __name__)

