from flask import Blueprint, jsonify, request
import uuid
from datetime import date

# entities
from models.entities.Scheduling import Scheduling

# models
from models.SchedulingModel import SchedulingModel

main = Blueprint('scheduling_routes_blueprint', __name__)

# routes    
@main.route("/add_schedule", methods=['POST'])
def add_client():

    req = request.json

    r_sch = Scheduling(str(uuid.uuid4()), user_id=req['user_id'], scheduling_state=req['state'], appointment_id=req['appointment_id'], 
                       chassis_number=req['chassis_number'], scheduling_date=str(date.today()), visible=True, images=req['images'],
                       videos=req['videos'], finish_date=None, return_date=None, km=None, details=None, document=None, cost=None)
    print(r_sch.to_JSON())
    try:
        affected_rows = SchedulingModel.add_schedule(r_sch)
        if affected_rows == 1: 
            return jsonify({'message': 'Scheduling added successfully', 'id': r_sch.id})
    except Exception as ex:
        return jsonify({'message': 'Error on insert'}), 500
    
@main.route("/get_schedule/<id>", methods=['GET'])
def get_schedule(id):
    try:
        schedule = SchedulingModel.get_schedule(id)
        if schedule != None: 
            return jsonify(schedule)
        else:
            return jsonify({})
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route("/get_schedules_by_user", methods=['GET'])
def get_schedules_by_user():
    req = request.json
    try:
        schedules = SchedulingModel.get_schedules_by_user(req['user_id'])
        return jsonify(schedules)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route("/get_schedules_by_state", methods=['GET'])
def get_schedules_by_state():
    req = request.json
    try:
        schedules = SchedulingModel.get_schedules_by_state(req['state'])
        return jsonify(schedules)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route("/update_schedule/<id>", methods=['POST'])
def update_schedule(id):

    req = request.json
    #print(str(req))
    #print(id)
    r_sch = Scheduling(scheduling_id=id, user_id=req['user_id'], scheduling_state=req['state'], visible=req['visible'], 
                       chassis_number=req['chassis_number'], images=req['images'], videos=req['videos'], 
                       appointment_id=None, scheduling_date=None, finish_date=None, return_date=None, km=None, 
                       details=None, document=None, cost=None)
    
    print(r_sch.to_JSON())
    try:
        affected_rows = SchedulingModel.update_schedule(r_sch)
        if affected_rows == 1: 
            return jsonify({'message': 'Scheduling updated successfully', 'id': id})
        else:
            return jsonify({'message': 'No scheduling updated'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route("/finish_schedule/<id>", methods=['POST'])
# scheduling_state 4 terminado 
def finish_schedule(id):

    req = request.json
    #print(str(req))
    #print(id)
    r_sch = Scheduling(scheduling_id=id, user_id=None, scheduling_state=str(4), visible=None, 
                       chassis_number=None, images=None, videos=None, appointment_id=None, scheduling_date=None,
                       finish_date=req['finish_date'], return_date=req['return_date'], km=req['km'], 
                       details=req['details'], document=req['document'], cost=req['cost'])
    
    print(r_sch.to_JSON())
    try:
        affected_rows = SchedulingModel.finish_schedule(r_sch)
        if affected_rows == 1: 
            return jsonify({'message': 'Scheduling finished successfully', 'id': id})
        else:
            return jsonify({'message': 'No scheduling finished'}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500