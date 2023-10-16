from flask import Flask, jsonify
from flask_cors import CORS
from config import config

# routes
from routes import api_routes
from routes import ClientRoutes
from routes import VehicleRoutes
from routes import AppointmentRoutes
from routes import SchedulingRoutes

app = Flask(__name__)
CORS(app, resources={r"/api/*":{"origins":"http://192.168.100.14:8888"}})

# bad or non existing endpoints
@app.errorhandler(404)
def error(e):
    return jsonify({'message': 'Url does not exist', 'status_code': 1002}), 404

if __name__ == "__main__":
    #app.config.from_object(config['development'])
    #app.run(debug=True, port=5000, host='0.0.0.0')
    #app.run(debug=config['development'].DEBUG, port=config['development'].PORT, host=config['development'].HOST)

    # blueprints
    app.register_blueprint(api_routes.main, url_prefix='/api')
    app.register_blueprint(ClientRoutes.main, url_prefix='/api')
    app.register_blueprint(VehicleRoutes.main, url_prefix='/api')
    app.register_blueprint(AppointmentRoutes.main, url_prefix='/api')
    app.register_blueprint(SchedulingRoutes.main, url_prefix='/api')
    
    #app.run()
    app.config['UPLOAD_FOLDER_IMG'] = config['development'].UPLOAD_FOLDER_IMG
    app.config['UPLOAD_FOLDER_VID'] = config['development'].UPLOAD_FOLDER_VID
    app.config['UPLOAD_FOLDER_DOC'] = config['development'].UPLOAD_FOLDER_DOC
    app.run(debug=config['development'].DEBUG, port=config['development'].PORT, host=config['development'].HOST)
