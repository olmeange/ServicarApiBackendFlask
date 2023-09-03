from flask import Blueprint, jsonify, request
import uuid

# entities
from models.entities.Vehicle import Vehicle

# models
from models.VehicleModel import VehicleModel

main = Blueprint('vehicle_routes_blueprint', __name__)

# routes
@main.route("/add_vehicle", methods=['POST'])
def add_vehicle():

    req = request.json

    r_vehicle = Vehicle(str(uuid.uuid4()), req['mark'], req['model'], req['year'], req['plate'], req['client_id'])
    print(r_vehicle.to_JSON())
    try:
        affected_rows = VehicleModel.add_vehicle(r_vehicle)
        if affected_rows == 1: 
            return jsonify({'message': 'Vehicle added successfully', 'id': r_vehicle.id})
    except Exception as ex:
        return jsonify({'message': 'Error on insert'}), 500

@main.route("/get_vehicle/<id>", methods=['GET'])
def get_vehicle(id):
    try:
        vehicle = VehicleModel.get_vehicle(id)
        if vehicle != None: 
            return jsonify(vehicle)
        else:
            return jsonify({})
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route("/vehicles", methods=['GET'])
def get_vehicles():
    try:
        vehicles = VehicleModel.get_vehicles()
        return jsonify(vehicles)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route("/delete_vehicle/<id>", methods=['POST'])
def delete_vehicle(id):
    try:
        affected_rows = VehicleModel.delete_vehicle(id)
        if affected_rows == 1: 
            return jsonify({'message': 'Vehicle deleted successfully', 'id': id})
        else:
            return jsonify({'message': 'No vehicle deleted'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route("/update_vehicle/<id>", methods=['POST'])
def update_vehicle(id):

    req = request.json
    r_vehicle = Vehicle(mark=req['mark'], model=req['model'], year=req['year'], 
                        plate=req['plate'], client_id=None, id=id)
    print(r_vehicle.to_JSON())
    try:
        affected_rows = VehicleModel.update_vehicle(r_vehicle)
        if affected_rows == 1: 
            return jsonify({'message': 'Vehicle updated successfully', 'id': id})
        else:
            return jsonify({'message': 'No vehicle updated'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
