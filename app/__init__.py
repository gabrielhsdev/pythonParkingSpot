from flask import Flask
from flask_cors import CORS

from app.controllers.floors_controller import FloorsBlueprint
from app.controllers.parking_spots_controller import ParkingSpotsBlueprint
from app.controllers.cars_controller import CarsBlueprint

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'
    
    # Enable CORS for all origins
    CORS(app, origins=["http://localhost:5001", "http://127.0.0.1:5001"])
    
    # Register the other blueprints with their respective prefixes
    app.register_blueprint(FloorsBlueprint, url_prefix='/api/floors')
    app.register_blueprint(ParkingSpotsBlueprint, url_prefix='/api/parking-spots')
    app.register_blueprint(CarsBlueprint, url_prefix='/api/cars')
    
    return app
