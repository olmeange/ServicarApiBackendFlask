import os
from flask import Blueprint, jsonify, request, send_file
import uuid
from datetime import date
from config import config
from moviepy.editor import *

# entities
from models.entities.Scheduling import Scheduling

# models
from models.SchedulingModel import SchedulingModel

main = Blueprint('scheduling_routes_blueprint', __name__)

# routes    
@main.route("/add_schedule", methods=['POST'])
def add_schedule():
    req = request.json
    # validate non null fields is needed...

    r_sch = Scheduling(str(uuid.uuid4()), user_id=req['user_id'], scheduling_state=str(1), appointment_id=req['appointment_id'], 
                       chassis_number=req['chassis_number'], scheduling_date=str(date.today()), visible=True, images=None,
                       videos=None, finish_date=None, return_date=None, km=req['km'], details=None, document=None, cost=None)
    print(r_sch.to_JSON())
    try:
        affected_rows = SchedulingModel.add_schedule(r_sch)
        if affected_rows == 1:
            return jsonify({'message': 'Scheduling added successfully', 'id': r_sch.id, 'status_code': 1000})
    except Exception as ex:
        #return jsonify({'message': 'Error on insert'}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500
    
@main.route("/get_schedule/<id>", methods=['GET'])
def get_schedule(id):
    try:
        schedule = SchedulingModel.get_schedule(id)
        if schedule != None: 
            return jsonify({'schedule': schedule, 'status_code': 1000})
        else:
            return jsonify({'message': 'No schedule exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500
    
@main.route("/get_schedules_by_user", methods=['GET'])
def get_schedules_by_user():
    req = request.json
    try:
        schedules = SchedulingModel.get_schedules_by_user(req['user_id'])
        if len(schedules) != 0:
            return jsonify({'schedules': schedules, 'status_code': 1000})
        else:
            return jsonify({'message': 'No schedules exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500
    
@main.route("/get_schedules_by_user/<page>", methods=['GET'])
def get_schedules_by_user_per_page(page):
    # cuando se usan parametros en los headers no se usa guion bajo
    req = request.headers
    try:
        schedules = SchedulingModel.get_schedules_by_user_per_page(str(req['userId']), page)
        if len(schedules) != 0:
            return jsonify({'message':'Success','schedules': schedules, 'status_code': 1000})
        else:
            return jsonify({'message': 'No schedules exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500

@main.route("/get_schedules_by_state", methods=['GET'])
def get_schedules_by_state():
    req = request.json
    try:
        schedules = SchedulingModel.get_schedules_by_state(req['state'])
        if len(schedules) != 0:
            return jsonify({'schedules': schedules, 'status_code': 1000})
        else:
            return jsonify({'message': 'No schedules exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500
    
@main.route("/get_schedules_by_state/<page>", methods=['GET'])
def get_schedules_by_state_per_page(page):
    req = request.json
    try:
        schedules = SchedulingModel.get_schedules_by_state_per_page(req['state'], page)
        if len(schedules) != 0:
            return jsonify({'schedules': schedules, 'status_code': 1000})
        else:
            return jsonify({'message': 'No schedules exist', 'status_code': 1004})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500

@main.route("/update_schedule/<id>", methods=['POST'])
def update_schedule(id):
    req = request.json
    
    r_sch = Scheduling(scheduling_id=id, user_id=req['user_id'], scheduling_state=req['state'], visible=req['visible'], 
                       chassis_number=req['chassis_number'], images=None, videos=None, 
                       appointment_id=None, scheduling_date=None, finish_date=None, return_date=None, km=req['km'], 
                       details=None, document=None, cost=None)
    
    print(r_sch.to_JSON())
    try:
        affected_rows = SchedulingModel.update_schedule(r_sch)
        if affected_rows == 1: 
            return jsonify({'message': 'Scheduling updated successfully', 'id': id, 'status_code': 1000})
        else:
            return jsonify({'message': 'No scheduling updated', 'status_code': 1007}), 404
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500

@main.route("/finish_schedule/<id>", methods=['POST'])
def finish_schedule(id):    
    req = request.json

    r_sch = Scheduling(scheduling_id=id, user_id=None, scheduling_state=str(4), visible=None, 
                       chassis_number=None, images=None, videos=None, appointment_id=None, scheduling_date=None,
                       finish_date=req['finish_date'], return_date=req['return_date'], km=req['km'], 
                       details=req['details'], document=None, cost=req['cost'])
    
    print(r_sch.to_JSON())
    try:
        affected_rows = SchedulingModel.finish_schedule(r_sch)
        if affected_rows == 1: 
            return jsonify({'message': 'Scheduling finished successfully', 'id': id, 'status_code': 1000})
        else:
            return jsonify({'message': 'No scheduling finished', 'status_code': 1007}), 404
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500
    
# server sends processed or stored image to client
@main.route('/image/<filename>', methods=['GET'])
def send_image(filename:str):
    return send_file(f'../uploads/images/{filename}')

@main.route('/delete_image/<id>', methods=['POST'])
def delete_image(id):
    req = request.json
    try:
        affected_rows = SchedulingModel.delete_image(req['image'], id)
        if affected_rows == 1:
            # delete image from storage
            os.remove(f'../uploads/images/'+ req['image'])
            return jsonify({'message': 'Image deleted successfully', 'status_code': 1000})
        else:
            return jsonify({'message': 'No image deleted', 'status_code': 1006}), 404
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500

@main.route('/add_image/<id>', methods=['POST'])
def add_image(id):
    image = request.files['image']

    # validate non null fields is needed...

    image_name = str(uuid.uuid4())
    image_name_ext = image_name + '.jpg'  
    try:
        affected_rows = SchedulingModel.add_image(image_name, id)
        if affected_rows == 1:
            # save image to storage
            image.save(os.path.join(config['development'].UPLOAD_FOLDER_IMG, image_name_ext))    
            return jsonify({'message': 'Image added successfully', 'image': image_name_ext, 'status_code': 1000})
        #else:
        #    return jsonify({'message': 'No image added', 'status_code': 1006}), 404
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500 

@main.route('/update_image', methods=['POST'])
def update_image():
    image = request.files['image']
    req_image_name = request.form.get('image_name')
    # validate non null fields is needed...
 
    try:
        # save image to storage
        image.save(os.path.join(config['development'].UPLOAD_FOLDER_IMG, req_image_name))    
        return jsonify({'message': 'Image updated successfully', 'image': req_image_name, 'status_code': 1000})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500            

# server sends processed or stored video to client
@main.route('/video/<filename>', methods=['GET'])
def send_video(filename:str):
    return send_file(f'../uploads/videos/{filename}')
    #return send_from_directory('../uploads/videos/', filename, as_attachment=False)

@main.route('/delete_video/<id>', methods=['POST'])
def delete_video(id):
    req = request.json
    try:
        affected_rows = SchedulingModel.delete_video(req['video'], id)
        if affected_rows == 1:
            # delete video from storage
            os.remove(f'../uploads/videos/'+ req['video'])
            return jsonify({'message': 'Video deleted successfully', 'status_code': 1000})
        else:
            return jsonify({'message': 'No video deleted', 'status_code': 1006}), 404
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500  
    
@main.route('/add_video/<id>', methods=['POST'])
def add_video(id):
    video = request.files['video']

    # validate non null fields is needed...
    video_name = str(uuid.uuid4())
    video_name_ext = video_name + '.mp4'  
    try:
        affected_rows = SchedulingModel.add_video(video_name, id)
        if affected_rows == 1:
            # save video to storage
            video.save(os.path.join(config['development'].UPLOAD_FOLDER_VID, video_name_ext))
            
            # getting thumbnail saved video
            clip = VideoFileClip(config['development'].UPLOAD_FOLDER_VID + '\\' + video_name_ext)
            clip.save_frame(config['development'].UPLOAD_FOLDER_THUMBNAIL + '\\' + video_name + '.jpg', t=1.00)

            return jsonify({'message': 'Video added successfully', 'video': video_name_ext, 'status_code': 1000})
        #else:
        #    return jsonify({'message': 'No video added'}), 404
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500 

@main.route('/update_video', methods=['POST'])
def update_video():
    video = request.files['video']
    req_video_name = request.form.get('video_name')
    # validate non null fields is needed...
 
    try:
        # save image to storage
        video.save(os.path.join(config['development'].UPLOAD_FOLDER_VID, req_video_name))    
        return jsonify({'message': 'Video updated successfully', 'video': req_video_name, 'status_code': 1000})
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500

@main.route('/add_document/<id>', methods=['POST'])
def add_document(id):
    image = request.files['document']

    # validate non null fields is needed...

    document_name = id + '.pdf'  
    try:
        affected_rows = SchedulingModel.add_document(document_name, id)
        if affected_rows == 1:
            # save image to storage
            image.save(os.path.join(config['development'].UPLOAD_FOLDER_DOC, document_name))    
            return jsonify({'message': 'Document added successfully', 'document': document_name, 'status_code': 1000})
        else:
            return jsonify({'message': 'No document added', 'status_code': 1008}), 404
    except Exception as ex:
        #return jsonify({'message': str(ex)}), 500
        return jsonify({'message': 'Internal server error', 'status_code': 1003}), 500

# server sends processed or stored image to client
@main.route('/thumbnail/<filename>', methods=['GET'])
def send_thumbnail(filename:str):
    return send_file(f'../uploads/thumbnails/{filename}')          