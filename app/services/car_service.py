from typing import List
from app.utils.types.models.car import Car
from app.utils.db_util import get_db_connection
from app.models.car_model import CarModel
from app.services.parking_spot_service import ParkingSpotService

class CarService:
    def __init__(self):
        self.connection, self.cursor = get_db_connection()

    def create_car(self, license_plate: str, parking_spot_id: int) -> Car:
        if not license_plate or not parking_spot_id:
            raise Exception("license_plate and parking_spot_id are required")
        
        if CarModel().get_parked_car_by_license_plate(license_plate):
            raise Exception(f"A car with license plate {license_plate} is already parked")
        
        if not ParkingSpotService().isSpotAvaliable(parking_spot_id):
            raise Exception(f"Parking spot with ID {parking_spot_id} is not available")

        car = CarModel().create_car(license_plate, parking_spot_id)
        return car
    
    def update_car_leave_at(self, car_id: int) -> Car:
        car = CarModel()

        isParked = car.get_parked_car_by_id(car_id)
        if not isParked:
            raise Exception(f"Car with ID {car_id} not found or is not parked")

        return car.update_car_leave_at(car_id)
    
    def update_car_parking_spot(self, car_id: int, spot_id: int) -> Car:
        car = CarModel().get_parked_car_by_id(car_id)
        if not car:
            raise Exception(f"Car with ID {car_id} not found or is not parked")

        if not ParkingSpotService().isSpotAvaliable(spot_id):
            raise Exception(f"Parking spot with ID {spot_id} is not available")
        
        self.cursor.execute("UPDATE cars SET parking_spot_id = %s WHERE id = %s", (spot_id, car_id))
        self.connection.commit()

        return CarModel().get_car_by_id(car_id)
