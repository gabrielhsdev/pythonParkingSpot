from flask import Blueprint, request
from app.views.base_view import BaseView
from app.models.car_model import CarModel
from app.services.car_service import CarService
from app.utils.types.models.car import Car
from app.utils.types.views.base_view.viewParams import ViewParams
from typing import List

CarsBlueprint = Blueprint("cars", __name__)

# Helper function to handle errors, abstracting the response creation
def handle_error(message: str, status: int = 500):
    return BaseView.render(ViewParams(data=None, status=status, message=message))

# Endpoint to fetch all cars
@CarsBlueprint.route("/", methods=["GET"])
def default():
    try:
        cars: List[Car] = CarModel().get_cars()
        return BaseView.render(ViewParams(data=cars))
    except Exception as e:
        return handle_error(str(e))

# Endpoint to fetch a car by its ID
@CarsBlueprint.route("/<int:car_id>", methods=["GET"])
def get_car_by_id(car_id: int):
    try:
        car: Car = CarModel().get_car_by_id(car_id)
        if not car:
            return handle_error(f"Car with ID {car_id} not found", status=404)
        return BaseView.render(ViewParams(data=car))
    except Exception as e:
        return handle_error(str(e))

# Endpoint to fetch all parked cars
@CarsBlueprint.route("/parked", methods=["GET"])
def get_parked_cars():
    try:
        cars: List[Car] = CarModel().get_parked_cars()
        return BaseView.render(ViewParams(data=cars))
    except Exception as e:
        return handle_error(str(e))

# Endpoint ( Service ) to create a new car given a license plate and parking spot ID
@CarsBlueprint.route("/", methods=["POST"])
def create_car():
    try:
        license_plate = request.json.get("license_plate")
        parking_spot_id = request.json.get("parking_spot_id")
        if not license_plate or not parking_spot_id:
            return handle_error("license_plate and parking_spot_id are required", status=400)
        
        car: Car = CarService().create_car(license_plate, parking_spot_id)

        if not car:
            return handle_error("Car could not be created")
        
        return BaseView.render(ViewParams(data=car))
    except Exception as e:
        return handle_error(str(e))
    
# Endpoint ( Service ) to update a car's leave_at timestamp
@CarsBlueprint.route("/<int:car_id>/leave_at", methods=["PUT"])
def update_car(car_id: int):
    try:
        car: Car = CarService().update_car_leave_at(car_id)

        return BaseView.render(ViewParams(data=car))
    except Exception as e:
        return handle_error(str(e))

# Endpoint ( Service ) to update car's parking spot
@CarsBlueprint.route("/<int:car_id>/parking_spot", methods=["PUT"])
def update_car_parking_spot(car_id: int):
    try:
        spot_id = request.json.get("spot_id")
        if not spot_id:
            return handle_error("spot_id is required", status=400)
        car: Car = CarService().update_car_parking_spot(car_id, spot_id)
        return BaseView.render(ViewParams(data=car))
    except Exception as e:
        return handle_error(str(e))
    
# Endpoint to delete a car
@CarsBlueprint.route("/<int:car_id_log>", methods=["DELETE"])
def delete_car(car_id_log: int):
    try:
        car: Car = CarModel().delete_car(car_id_log)
        if not car:
            return handle_error(f"Car with ID {car_id_log} not found", status=404)
        return BaseView.render(ViewParams(data=None))
    except Exception as e:
        return handle_error(str(e))