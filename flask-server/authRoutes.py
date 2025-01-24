from flask import Blueprint, request, jsonify

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
