from flask import Blueprint, jsonify, request
#from datetime import date

# entities
#from models.entities.Client import Client

# models
from models.UserModel import UserModel
from models.LocationModel import LocationModel
from models.MaintenanceModel import MaintenanceModel

main = Blueprint('routes_blueprint', __name__)

# routes a construir
# Request Body Application/Json
# user_name (string) mandatory
# password (string) mandatory

@main.route("/login", methods=['POST'])
def login():
    req = request.json
    
    try:
        user = UserModel.login(req['user_name'], req['password'])
        return jsonify({'user': user, 'status_code': 1000})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'User does not exist', 'status_code': 1001}), 500

@main.route("/users", methods=['GET'])
def users():

    try:
        users = UserModel.get_users()
        if len(users) != 0:
            return jsonify({'users': users, 'status_code': 1000})
        else:
            return jsonify({'message': 'No users exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500

@main.route("/users/<page>", methods=['GET'])
def users_per_page(page):

    try:
        users = UserModel.get_users_per_page(page)
        if len(users) != 0:
            return jsonify({'users': users, 'status_code': 1000})
        else:
            return jsonify({'message': 'No users exist', 'status_code': 1004})
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
        #return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500

@main.route("/locations", methods=['GET'])
def locations():

    try:
        locations = LocationModel.get_locations()
        if len(locations) != 0:
            return jsonify({'locations': locations, 'status_code': 1000})
        else:
            return jsonify({'message': 'No locations exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500
    
@main.route("/maintenances", methods=['GET'])
def maintenances():

    try:
        maintenances = MaintenanceModel.get_maintenances()
        if len(maintenances) != 0:
            return jsonify({'maintenances': maintenances, 'status_code': 1000})
        else:
            return jsonify({'message': 'No maintenances exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500