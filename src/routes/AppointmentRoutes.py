from flask import Blueprint, jsonify, request, render_template
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
                                location_id=req['location_id'], mainteinance_id=req['mainteinance_id'], date=str(date.today()), visible=True, user_id=req['user_id'])
    print(r_appointment.to_JSON())
    try:
        affected_rows = AppointmentModel.add_appointment(r_appointment)
        if affected_rows[0] == 1: 
            return jsonify({'message': 'Appointment added successfully', 'id': r_appointment.id, 'status_code': 1000})
    except Exception as ex:
        #return jsonify({'message': 'Error on insert'}), 500
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500
    
@main.route("/form")
def appointment_form():
    return render_template('appointment_form.html')

@main.route("/add_appointment_from_client", methods=['POST'])
def add_appointment_from_client():
    r_appointment = Appointment(id=str(uuid.uuid4()), first_name=request.form['first_name'], last_name=request.form['last_name'], 
                                document_id=request.form['document_id'], address=request.form['address'], email=request.form['email'], 
                                phone=request.form['phone'], mark=request.form['mark'], model=request.form['model'], 
                                plate=request.form['plate'], year=request.form['year'], location_id=request.form['location_id'], 
                                mainteinance_id=request.form['mainteinance_id'], date=str(date.today()), visible=True)
    print(r_appointment.to_JSON())
    try:
        affected_rows = AppointmentModel.add_appointment(r_appointment)
        if affected_rows[0] == 1: 
            return jsonify({'message': 'Appointment added successfully', 'id': r_appointment.id, 'status_code': 1000})
    except Exception as ex:
        #return jsonify({'message': 'Error on insert'}), 500
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500
    #return "received"

@main.route("/get_appointment/<id>", methods=['GET'])
def get_appointment(id):
    try:
        appointment = AppointmentModel.get_appointment(id)
        if appointment != None: 
            return jsonify({'appointment': appointment, 'status_code': 1000})
        else:
            return jsonify({'message': 'Appointment does not exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500
    
@main.route("/appointments", methods=['GET'])
def get_appointments():
    try:
        appointments = AppointmentModel.get_appointments()
        if len(appointments) != 0:
            return jsonify({'appointments': appointments, 'status_code': 1000})
        else:
            return jsonify({'message': 'No appointments exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500
    
@main.route("/appointments/<page>", methods=['GET'])
def get_appointments_per_page(page):
    try:
        appointments = AppointmentModel.get_appointments_per_page(page)
        if len(appointments) != 0:
            return jsonify({'message':'Success', 'appointments': appointments, 'status_code': 1000})
        else:
            return jsonify({'message': 'No appointments exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500

@main.route("/update_appointment/<id>", methods=['POST'])
def update_appointment(id):

    req = request.json
    req_header = request.headers    
    r_appointment = Appointment(first_name=req['first_name'], last_name=req['last_name'], document_id= req['document_id'], 
                                address=req['address'], email=req['email'], phone=req['phone'],
                                mark=req['mark'], model=req['model'], plate=req['plate'], year=req['year'], 
                                location_id=req['location_id'], mainteinance_id=req['mainteinance_id'], date=None, 
                                visible=req['visible'], id=id, user_id=req['user_id'])
    print(r_appointment.to_JSON())
    try:
        affected_rows = AppointmentModel.update_appointment(r_appointment, req_header['userId'])
        if affected_rows == 1: 
            return jsonify({'message': 'Appointment updated successfully', 'id': id, 'status_code': 1000})
        else:
            return jsonify({'message': 'No appointment updated', 'status_code': 1007}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
        #return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500
    
@main.route("/appointments_user", methods=['GET'])
def get_appointments_user():
    req = request.headers
    try:
        appointments = AppointmentModel.get_appointments_user(req['userId'])
        if len(appointments) != 0:
            return jsonify({'appointments': appointments, 'status_code': 1000})
        else:
            return jsonify({'message': 'No appointments exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500
    
@main.route("/appointments_user/<page>", methods=['GET'])
def get_appointments_user_per_page(page):
    req = request.headers
    try:
        appointments = AppointmentModel.get_appointments_user_per_page(req['userId'], page)
        if len(appointments) != 0:
            return jsonify({'message':'Success', 'appointments': appointments, 'status_code': 1000})
        else:
            return jsonify({'message': 'No appointments exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500