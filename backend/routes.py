from flask import Blueprint, request, jsonify
from cinema_functions_for_database import get_seats_for_hall

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['POST'])

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        return jsonify({"success": True, "message": "Login Successful"})
    else:
        return jsonify({"success": False, "message": "Login Failed"})

seats_routes = Blueprint('seats_routes', __name__)

@seats_routes.route('/seats', methods=['GET'])

def api_get_seats():
    hall_id = request.args.get('hall_id')
    if not hall_id:
        return jsonify({"error": "hall_id parameter is required"}), 400
    seats = get_seats_for_hall(hall_id)
    return jsonify(seats)