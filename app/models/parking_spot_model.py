from typing import List
from app.utils.db_util import get_db_connection
from app.utils.types.models.parkingSpot import ParkingSpot

class ParkingSpotModel:

    def __init__(self):
        """
        Initializes the ParkingSpotModel with a database connection and cursor.
        """
        self.connection, self.cursor = get_db_connection()  # Initialize connection and cursor once
    
    def get_parking_spots(self) -> List[ParkingSpot]:
        """
        Fetches all parking spots from the database and returns a list of ParkingSpot objects.
        
        Returns:
            List[ParkingSpot]: A list of ParkingSpot objects representing all parking spots in the database.
        """
        self.cursor.execute("SELECT * FROM parking_spots")
        rows = self.cursor.fetchall()  # This will be a list of dictionaries

        # Convert rows (dictionaries) to ParkingSpot objects
        parking_spots = [ParkingSpot(**row) for row in rows]  # Unpack dictionary directly into ParkingSpot
        return parking_spots

    def get_parking_spot_by_id(self, spot_id: int) -> ParkingSpot:
        """
        Fetches a parking spot by its ID.
        
        Args:
            spot_id (int): The ID of the parking spot to fetch.
        
        Returns:
            ParkingSpot: The parking spot object corresponding to the provided ID.
        """
        self.cursor.execute("SELECT * FROM parking_spots WHERE id = %s", (spot_id,))
        row = self.cursor.fetchone()
        
        if row:
            return ParkingSpot(**row)
        return None
    
    def create_parking_spot(self, floor_id: int, spot_number: str) -> ParkingSpot:
        """
        Creates a new parking spot and inserts it into the database.
        
        Args:
            floor_id (int): The ID of the floor where the parking spot is located.
            spot_number (str): The unique identifier for the parking spot (e.g. "A1", "B12").
        
        Returns:
            ParkingSpot: The newly created ParkingSpot object.
        """
        self.cursor.execute(
            "INSERT INTO parking_spots (floor_id, spot_number) VALUES (%s, %s)",
            (floor_id, spot_number)
        )
        self.connection.commit()  # Commit the changes to the database
        
        # Fetch the newly created parking spot from the DB
        self.cursor.execute("SELECT * FROM parking_spots WHERE spot_number = %s AND floor_id = %s", (spot_number, floor_id))
        row = self.cursor.fetchone()
        
        if row:
            return ParkingSpot(**row)
        return None
    
    def update_parking_spot(self, spot_id: int, floor_id: int, spot_number: str) -> ParkingSpot:
        """
        Updates an existing parking spot in the database.
        
        Args:
            spot_id (int): The ID of the parking spot to update.
            floor_id (int): The ID of the floor where the parking spot is located.
            spot_number (str): The unique identifier for the parking spot (e.g. "A1", "B12").
        
        Returns:
            ParkingSpot: The updated ParkingSpot object.
        """
        self.cursor.execute(
            "UPDATE parking_spots SET floor_id = %s, spot_number = %s WHERE id = %s",
            (floor_id, spot_number, spot_id)
        )
        self.connection.commit()

        # Fetch the updated parking spot from the DB
        self.cursor.execute("SELECT * FROM parking_spots WHERE id = %s", (spot_id,))
        row = self.cursor.fetchone()

        if row:
            return ParkingSpot(**row)
        else:
            return None

    def delete_parking_spot(self, spot_id: int) -> bool:
        """
        Deletes a parking spot from the database.
        
        Args:
            spot_id (int): The ID of the parking spot to delete.
        
        Returns:
            bool: True if the parking spot was deleted, False otherwise.
        """
        self.cursor.execute("DELETE FROM parking_spots WHERE id = %s", (spot_id,))
        self.connection.commit()  # Commit the changes to the database
        
        # Return True if the spot was deleted, False otherwise
        return self.cursor.rowcount > 0