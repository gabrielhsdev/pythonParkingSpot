from flask import Blueprint, request
from app.views.base_view import BaseView
from app.models.parking_spot_model import ParkingSpotModel
from app.services.parking_spot_service import ParkingSpotService
from app.utils.types.models.parkingSpot import ParkingSpot
from app.utils.types.views.base_view.viewParams import ViewParams
from typing import List

ParkingSpotsBlueprint = Blueprint("parking_spots", __name__)

# Helper function to handle errors, abstracting the response creation
def handle_error(message: str, status: int = 500):
    return BaseView.render(ViewParams(data=None, status=status, message=message))

# Endpoint to fetch all parking spots
@ParkingSpotsBlueprint.route("/", methods=["GET"])
def default():
    try:
        parking_spots: List[ParkingSpot] = ParkingSpotModel().get_parking_spots()
        return BaseView.render(ViewParams(data=parking_spots))
    except Exception as e:
        return handle_error(str(e))
    
# Endpoint to fetch a parking spot by its ID
@ParkingSpotsBlueprint.route("/<int:spot_id>", methods=["GET"])
def get_parking_spot_by_id(spot_id: int):
    try:
        parking_spot: ParkingSpot = ParkingSpotModel().get_parking_spot_by_id(spot_id)
        if not parking_spot:
            return handle_error(f"Parking spot with ID {spot_id} not found", status=404)
        return BaseView.render(ViewParams(data=parking_spot))
    except Exception as e:
        return handle_error(str(e))

# Endpoint to create a new parking spot
@ParkingSpotsBlueprint.route("/", methods=["POST"])
def create_parking_spot():
    try:
        floor_id = request.json.get("floor_id")
        spot_number = request.json.get("spot_number")
        if not floor_id or not spot_number:
            return handle_error("floor_id and spot_number are required", status=400)
        parking_spot: ParkingSpot = ParkingSpotModel().create_parking_spot(floor_id, spot_number)
        return BaseView.render(ViewParams(data=parking_spot))
    except Exception as e:
        return handle_error(str(e))

# Endpoint to update a parking spot
@ParkingSpotsBlueprint.route("/<int:spot_id>", methods=["PUT"])
def update_parking_spot(spot_id: int):
    try:
        floor_id = request.json.get("floor_id")
        spot_number = request.json.get("spot_number")
        parking_spot: ParkingSpot = ParkingSpotModel().update_parking_spot(spot_id, floor_id, spot_number)
        if not parking_spot:
            return handle_error(f"Parking spot with ID {spot_id} not found", status=404)
        return BaseView.render(ViewParams(data=parking_spot))
    except Exception as e:
        return handle_error(str(e))

# Endpoint to delete a parking spot
@ParkingSpotsBlueprint.route("/<int:spot_id>", methods=["DELETE"])
def delete_parking_spot(spot_id: int):
    try:
        parking_spot: ParkingSpot = ParkingSpotModel().delete_parking_spot(spot_id)
        if not parking_spot:
            return handle_error(f"Parking spot with ID {spot_id} not found", status=404)
        return BaseView.render(ViewParams(data=parking_spot))
    except Exception as e:
        return handle_error(str(e))

# Endpoint ( Service ) to check if a parking spot is available
@ParkingSpotsBlueprint.route("/isAvailable/<int:spot_id>", methods=["GET"])
def is_spot_available(spot_id: int):
    try:
        is_available: bool = ParkingSpotService().isSpotAvaliable(spot_id)
        return BaseView.render(ViewParams(data=is_available))
    except Exception as e:
        return handle_error(str(e))
    
# Endpoint ( Service ) to get parking spot history
@ParkingSpotsBlueprint.route("/history/<int:spot_id>", methods=["GET"])
def get_parking_spot_history(spot_id: int):
    try:
        parking_spot: ParkingSpot = ParkingSpotService().getParkingSpotHistory(spot_id)
        if not parking_spot:
            return handle_error(f"Parking spot with ID {spot_id} history not found", status=404)
        return BaseView.render(ViewParams(data=parking_spot))
    except Exception as e:
        return handle_error(str(e))
