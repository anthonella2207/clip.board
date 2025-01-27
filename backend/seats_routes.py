from flask import Blueprint, request, jsonify
from cinema_functions_for_database import get_seats_for_hall

seats_routes = Blueprint('seats_routes', __name__)

@seats_routes.route('/seats', methods=['GET'])

def api_get_seats():
    hall_id = request.args.get('hall_id')
    if not hall_id:
        return jsonify({"error": "hall_id parameter is required"}), 400
    seats = get_seats_for_hall(hall_id)
    return jsonify(seats)