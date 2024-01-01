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
            return jsonify({'message': 'Vehicle added successfully', 'id': r_vehicle.id, 'status_code': 1000})
    except Exception as ex:
        #return jsonify({'message': 'Error on insert'}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500 

@main.route("/get_vehicle/<id>", methods=['GET'])
def get_vehicle(id):
    try:
        vehicle = VehicleModel.get_vehicle(id)
        if vehicle != None: 
            return jsonify({'vehicle': vehicle, 'status_code': 1000})
        else:
            return jsonify({'message': 'No vehicle exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500 
    
@main.route("/vehicles", methods=['GET'])
def get_vehicles():
    try:
        vehicles = VehicleModel.get_vehicles()
        if len(vehicles) !=0:
            return jsonify({'vehicles': vehicles, 'status_code': 1000})
        else:
            return jsonify({'message': 'No vehicles exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500

@main.route("/vehicles/<page>", methods=['GET'])
def get_vehicles_per_page(page):
    try:
        vehicles = VehicleModel.get_vehicles_per_page(page)
        if len(vehicles) !=0:
            return jsonify({'message':'Success', 'vehicles': vehicles, 'status_code': 1000})
        else:
            return jsonify({'message': 'No vehicles exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500  
    
@main.route("/delete_vehicle/<id>", methods=['POST'])
def delete_vehicle(id):
    try:
        affected_rows = VehicleModel.delete_vehicle(id)
        if affected_rows == 1: 
            return jsonify({'message': 'Vehicle deleted successfully', 'id': id, 'status_code': 1000})
        else:
            return jsonify({'message': 'No vehicle deleted', 'status_code': 1006}), 404
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500 
    
@main.route("/update_vehicle/<id>", methods=['POST'])
def update_vehicle(id):

    req = request.json
    r_vehicle = Vehicle(mark=req['mark'], model=req['model'], year=req['year'], 
                        plate=req['plate'], client_id=None, id=id)
    print(r_vehicle.to_JSON())
    try:
        affected_rows = VehicleModel.update_vehicle(r_vehicle)
        if affected_rows == 1: 
            return jsonify({'message': 'Vehicle updated successfully', 'id': id, 'status_code': 1000})
        else:
            return jsonify({'message': 'No vehicle updated', 'status_code': 1007}), 404
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500 