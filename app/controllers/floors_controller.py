from typing import List
from flask import Blueprint, request
from app.views.base_view import BaseView
from app.models.floor_model import FloorModel
from app.utils.types.models.floor import Floor
from app.utils.types.views.base_view.viewParams import ViewParams

FloorsBlueprint = Blueprint("floors", __name__)

# Helper function to handle errors, abstracting the response creation
def handle_error(message: str, status: int = 500):
    return BaseView.render(ViewParams(data=None, status=status, message=message))

# Endpoint to fetch all floors
@FloorsBlueprint.route("/", methods=["GET"])
def default():
    try:
        floors: List[Floor] = FloorModel().get_floors()
        return BaseView.render(ViewParams(data=floors))
    except Exception as e:
        return handle_error(str(e))

# Endpoint to fetch a floor by its ID
@FloorsBlueprint.route("/<int:floor_id>", methods=["GET"])
def get_floor_by_id(floor_id: int):
    try:
        floor: Floor = FloorModel().get_floor_by_id(floor_id)
        if not floor:
            return handle_error(f"Floor with ID {floor_id} not found", status=404)
        return BaseView.render(ViewParams(data=floor))
    except Exception as e:
        return handle_error(str(e))

# Endpoint to create a new floor
@FloorsBlueprint.route("/", methods=["POST"])
def create_floor():
    try:
        floor_number = request.json.get("floor_number")
        floor_name = request.json.get("floor_name")
        if not floor_number or not floor_name:
            return handle_error("floor_number and floor_name are required", status=400)
        floor: Floor = FloorModel().create_floor(floor_number, floor_name)
        return BaseView.render(ViewParams(data=floor))
    except Exception as e:
        return handle_error(str(e))

# Endpoint to update a floor
@FloorsBlueprint.route("/<int:floor_id>", methods=["PUT"])
def update_floor(floor_id: int):
    try:
        floor_number = request.json.get("floor_number")
        floor_name = request.json.get("floor_name")
        floor: Floor = FloorModel().update_floor(floor_id, floor_number, floor_name)
        if not floor:
            return handle_error(f"Floor with ID {floor_id} not found", status=404)
        return BaseView.render(ViewParams(data=floor))
    except Exception as e:
        return handle_error(str(e))

# Endpoint to delete a floor
@FloorsBlueprint.route("/<int:floor_id>", methods=["DELETE"])
def delete_floor(floor_id: int):
    try:
        result = FloorModel().delete_floor(floor_id)
        if not result:
            return handle_error(f"Floor with ID {floor_id} not found", status=404)
        return BaseView.render(ViewParams(data=None))
    except Exception as e:
        return handle_error(str(e))
