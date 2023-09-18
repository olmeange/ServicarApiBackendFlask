from flask import Blueprint, jsonify, request
import uuid

# entities
from models.entities.Client import Client

# models
from models.ClientModel import ClientModel

main = Blueprint('client_routes_blueprint', __name__)

# routes    
@main.route("/add_client", methods=['POST'])
def add_client():

    req = request.json

    r_client = Client(str(uuid.uuid4()), first_name=req['first_name'], last_name=req['last_name'], address=req['address'], phone=req['phone'], email=req['email'], document_id=req['document_id'])
    print(r_client.to_JSON())
    try:
        affected_rows = ClientModel.add_client(r_client)
        if affected_rows == 1: 
            return jsonify({'message': 'Client added successfully', 'id': r_client.id})
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
        #return jsonify({'message': 'Error on insert'}), 500

@main.route("/get_client/<id>", methods=['GET'])
def get_client(id):
    try:
        client = ClientModel.get_client(id)
        if client != None: 
            return jsonify(client)
        else:
            return jsonify({})
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route("/clients", methods=['GET'])
def get_clients():
    try:
        clients = ClientModel.get_clients()
        return jsonify(clients)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route("/delete_client/<id>", methods=['POST'])
def delete_client(id):
    try:
        affected_rows = ClientModel.delete_client(id)
        if affected_rows == 1: 
            return jsonify({'message': 'Client deleted successfully', 'id': id})
        else:
            return jsonify({'message': 'No client deleted'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route("/update_client/<id>", methods=['POST'])
def update_client(id):

    req = request.json
    r_client = Client(first_name=req['first_name'], last_name=req['last_name'], address=req['address'], phone=req['phone'], email=req['email'], document_id=req['document_id'], client_code=req['client_code'], id=id)
    print(r_client.to_JSON())
    try:
        affected_rows = ClientModel.update_client(r_client)
        if affected_rows == 1: 
            return jsonify({'message': 'Client updated successfully', 'id': id})
        else:
            return jsonify({'message': 'No client updated'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
