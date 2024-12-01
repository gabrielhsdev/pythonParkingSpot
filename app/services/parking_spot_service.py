from typing import List
from app.utils.db_util import get_db_connection
from app.utils.types.models.parkingSpot import ParkingSpot
from app.utils.types.models.car import Car
from app.models.parking_spot_model import ParkingSpotModel

class ParkingSpotService:
    def __init__(self):
        self.connection, self.cursor = get_db_connection()
    
    def isSpotAvaliable(self, spot_id: int) -> bool:
        self.cursor.execute("SELECT * FROM cars WHERE parking_spot_id = %s AND leave_at IS NULL", (spot_id,))
        row = self.cursor.fetchone()

        if row:
            return False
        else :
            return True
        
    def getParkingSpotHistory(self, spot_id: int) -> List[ParkingSpot]:
        self.cursor.execute("SELECT * FROM cars WHERE parking_spot_id = %s", (spot_id,))
        rows = self.cursor.fetchall()
        
        cars = [Car(**row) for row in rows]  # Unpack dictionary directly into Car
        return cars