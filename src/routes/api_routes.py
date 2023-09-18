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
        return jsonify(user)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route("/users", methods=['GET'])
def users():

    try:
        users = UserModel.get_users()
        return jsonify(users)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route("/locations", methods=['GET'])
def locations():

    try:
        locations = LocationModel.get_locations()
        return jsonify(locations)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route("/maintenances", methods=['GET'])
def maintenances():

    try:
        maintenances = MaintenanceModel.get_maintenances()
        return jsonify(maintenances)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500