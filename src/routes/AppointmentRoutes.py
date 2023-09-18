from flask import Blueprint, jsonify, request
import uuid
from datetime import date

# entities
from models.entities.Appointment import Appointment

# models
from models.AppointmentModel import AppointmentModel

main = Blueprint('appointment_routes_blueprint', __name__)

@main.route("/add_appointment", methods=['POST'])
def add_appointment():

    req = request.json
    r_appointment = Appointment(id=str(uuid.uuid4()), first_name=req['first_name'], last_name=req['last_name'], 
                                document_id=req['document_id'], address=req['address'], email=req['email'], phone=req['phone'],
                                mark=req['mark'], model=req['model'], plate=req['plate'], year=req['year'], 
                                location_id=req['location_id'], mainteinance_id=req['mainteinance_id'], date=str(date.today()), visible=True)
    print(r_appointment.to_JSON())
    try:
        affected_rows = AppointmentModel.add_appointment(r_appointment)
        if affected_rows[0] == 1: 
            return jsonify({'message': 'Appointment added successfully', 'id': r_appointment.id})
    except Exception as ex:
        #return jsonify({'message': 'Error on insert'}), 500
        return jsonify({'message': str(ex)}), 500

@main.route("/get_appointment/<id>", methods=['GET'])
def get_appointment(id):
    try:
        appointment = AppointmentModel.get_appointment(id)
        if appointment != None: 
            return jsonify(appointment)
        else:
            return jsonify({})
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route("/appointments", methods=['GET'])
def get_appointments():
    try:
        appointments = AppointmentModel.get_appointments()
        return jsonify(appointments)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route("/update_appointment/<id>", methods=['POST'])
def update_appointment(id):

    req = request.json
    r_appointment = Appointment(first_name=req['first_name'], last_name=req['last_name'], document_id= req['document_id'], 
                                address=req['address'], email=req['email'], phone=req['phone'],
                                mark=req['mark'], model=req['model'], plate=req['plate'], year=req['year'], 
                                location_id=req['location_id'], mainteinance_id=req['mainteinance_id'], date=None, 
                                visible=req['visible'], id=id)
    print(r_appointment.to_JSON())
    try:
        affected_rows = AppointmentModel.update_appointment(r_appointment)
        if affected_rows == 1: 
            return jsonify({'message': 'Appointment updated successfully', 'id': id})
        else:
            return jsonify({'message': 'No appointment updated'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500