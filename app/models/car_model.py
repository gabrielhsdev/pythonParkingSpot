from typing import List, Optional, Union
from app.utils.db_util import get_db_connection
from app.utils.types.models.car import Car

class CarModel:

    def __init__(self):
        """
        Initializes the CarModel with a database connection and cursor.
        """
        self.connection, self.cursor = get_db_connection()  # Initialize connection and cursor once

    def get_cars(self) -> List[Car]:
        """
        Fetches all cars from the database and returns a list of Car objects.
        
        Returns:
            List[Car]: A list of Car objects representing all cars in the database.
        """
        self.cursor.execute("SELECT * FROM cars")
        rows = self.cursor.fetchall()  # This will be a list of dictionaries

        # Convert rows (dictionaries) to Car objects
        cars = [Car(**row) for row in rows]  # Unpack dictionary directly into Car
        return cars

    def get_car_by_id(self, car_id: int) -> Optional[Car]:
        """
        Fetches a car by its ID.
        
        Args:
            car_id (int): The ID of the car to fetch.
        
        Returns:
            Optional[Car]: The Car object corresponding to the provided ID, or None if not found.
        """
        self.cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
        row = self.cursor.fetchone()
        
        if row:
            return Car(**row)
        return None

    def get_parked_car_by_id(self, car_id: int) -> Optional[Car]:
        """
        Fetches a parked car by its ID.
        
        Args:
            car_id (int): The ID of the car to fetch.
        
        Returns:
            Optional[Car]: The Car object corresponding to the provided ID, or None if not found.
        """
        self.cursor.execute("SELECT * FROM cars WHERE id = %s AND leave_at IS NULL", (car_id,))
        row = self.cursor.fetchone()
        
        if row:
            return Car(**row)
        return None

    def get_parked_car_by_license_plate(self, license_plate: str) -> Optional[Car]:
        """
        Fetches a parked car by its license plate.
        
        Args:
            license_plate (str): The license plate of the car to fetch.
        
        Returns:
            Optional[Car]: The Car object corresponding to the provided license plate, or None if not found.
        """
        self.cursor.execute("SELECT * FROM cars WHERE license_plate = %s AND leave_at IS NULL", (license_plate,))
        row = self.cursor.fetchone()
        
        if row:
            return Car(**row)
        return None

    def get_parked_cars(self) -> List[Car]:
        """
        Fetches all cars that are currently parked in the parking lot.
        
        Returns:
            List[Car]: A list of Car objects representing all parked cars.
        """
        self.cursor.execute("SELECT * FROM cars WHERE leave_at IS NULL")
        rows = self.cursor.fetchall()

        cars = [Car(**row) for row in rows]  # Unpack dictionary directly into Car
        return cars

    def create_car(self, license_plate: str, parking_spot_id: int) -> Optional[Car]:
        """
        Adds a new car to the parking spot.
        
        Args:
            license_plate (str): The license plate of the car.
            parking_spot_id (int): The ID of the parking spot where the car will be parked.
        
        Returns:
            Optional[Car]: The newly created Car object, or None if the operation failed.
        """
        self.cursor.execute(
            "INSERT INTO cars (license_plate, parking_spot_id) VALUES (%s, %s)",
            (license_plate, parking_spot_id)
        )
        self.connection.commit()  # Commit the changes to the database
        
        # Fetch the newly added car from the DB
        self.cursor.execute("SELECT * FROM cars WHERE license_plate = %s", (license_plate,))
        row = self.cursor.fetchone()
        
        if row:
            return Car(**row)
        return None
    
    def update_car_leave_at(self, car_id: int) -> Optional[Car]:
        """
        Updates the leave_at timestamp of a parked car.
        
        Args:
            car_id (int): The ID of the car to update.
        
        Returns:
            Optional[Car]: The updated Car object, or None if the operation failed.
        """
        self.cursor.execute("UPDATE cars SET leave_at = NOW() WHERE id = %s", (car_id,))
        self.connection.commit()

        # Fetch the updated car from the DB
        self.cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
        row = self.cursor.fetchone()

        if row:
            return Car(**row)
        return None
    
    def update_car_spot(self, car_id: int, spot_id: int) -> Optional[Car]:
        """
        Updates the parking spot of a parked car.
        
        Args:
            car_id (int): The ID of the car to update.
            spot_id (int): The ID of the new parking spot.
        
        Returns:
            Optional[Car]: The updated Car object, or None if the operation failed.
        """
        self.cursor.execute("UPDATE cars SET parking_spot_id = %s WHERE id = %s", (spot_id, car_id))
        self.connection.commit()

        # Fetch the updated car from the DB
        self.cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
        row = self.cursor.fetchone()

        if row:
            return Car(**row)
        return None
    
    def delete_car(self, id: int) -> bool:
        """
        Deletes a car from the database.
        
        Args:
            id (int): The ID of the car log to delete.
        
        Returns:
            bool: True if the car was deleted, False otherwise.
        """
        self.cursor.execute("DELETE FROM cars WHERE id = %s", (id,))
        self.connection.commit()  # Commit the changes to the database
        
        # Return True if the car was deleted, False otherwise
        return self.cursor.rowcount > 0
