from flask import Flask
from flask_cors import CORS
from config import config

# routes
from routes import api_routes
from routes import ClientRoutes
from routes import VehicleRoutes
from routes import AppointmentRoutes

app = Flask(__name__)
CORS(app, resources={"*":{"origins":"http://192.168.100.14:57280"}})

if __name__ == "__main__":
    #app.config.from_object(config['development'])
    #app.run(debug=True, port=5000, host='0.0.0.0')
    #app.run(debug=config['development'].DEBUG, port=config['development'].PORT, host=config['development'].HOST)

    # blueprints
    app.register_blueprint(api_routes.main, url_prefix='/api')
    app.register_blueprint(ClientRoutes.main, url_prefix='/api')
    app.register_blueprint(VehicleRoutes.main, url_prefix='/api')
    app.register_blueprint(AppointmentRoutes.main, url_prefix='/api')
    #app.run()
    app.run(debug=config['development'].DEBUG, port=config['development'].PORT, host=config['development'].HOST)
