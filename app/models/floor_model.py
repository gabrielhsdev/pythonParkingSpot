from typing import List
from app.utils.types.models.floor import Floor
from app.utils.db_util import get_db_connection

class FloorModel:

    def __init__(self):
        """
        Initializes the FloorModel with a database connection and cursor.
        """
        self.connection, self.cursor = get_db_connection()

    def close(self):
        """
        Closes the database connection and cursor when done.
        """
        self.cursor.close()  # Close cursor
        self.connection.close()  # Close the connection

    def get_floors(self) -> List[Floor]:
        """
        Fetches all floors from the database and returns a list of Floor objects.
        
        Returns:
            List[Floor]: A list of Floor objects representing all the floors in the database.
        """
        self.cursor.execute("SELECT * FROM floors")
        rows = self.cursor.fetchall()  # This will be a list of dictionaries

        floors = [Floor(**row) for row in rows] 
        return floors

    def get_floor_by_id(self, floor_id: int) -> Floor:
        """
        Fetches a single floor by its ID from the database and returns a Floor object.
        
        Args:
            floor_id (int): The ID of the floor to retrieve.
        
        Returns:
            Floor: A Floor object representing the floor with the given ID.
        """
        self.cursor.execute("SELECT * FROM floors WHERE id = %s", (floor_id,))
        row = self.cursor.fetchone()  # Fetch a single row

        if row:
            return Floor(**row)  # Return the Floor object using the row data
        else:
            return None  # Return None if the floor with the given ID was not found

    def create_floor(self, floor_number: int, floor_name: str) -> Floor:
        """
        Creates a new floor in the database with the provided floor number and name.
        
        Args:
            floor_number (int): The number of the floor to create.
            floor_name (str): The name of the floor to create.
        
        Returns:
            Floor: The newly created Floor object.
        """
        # Insert the new floor into the database
        self.cursor.execute(
            "INSERT INTO floors (level, name) VALUES (%s, %s)",  # Map floor_number to level and floor_name to name
            (floor_number, floor_name)
        )
        self.connection.commit()

        # Retrieve the newly created floor
        self.cursor.execute("SELECT * FROM floors WHERE level = %s", (floor_number,))
        row = self.cursor.fetchone()


        if row:
            return Floor(**row)
        else:
            return None
        
    def delete_floor(self, floor_id: int) -> bool:
        """
        Deletes a floor from the database based on its ID.
        
        Args:
            floor_id (int): The ID of the floor to delete.
        
        Returns:
            bool: True if the floor was successfully deleted, False otherwise.
        """
        self.cursor.execute("DELETE FROM floors WHERE id = %s", (floor_id,))
        self.connection.commit()

        return self.cursor.rowcount > 0

    def update_floor(self, floor_id: int, floor_number: int, floor_name: str) -> Floor:
        """
        Updates the floor with the given ID in the database with the new floor number and name.
        
        Args:
            floor_id (int): The ID of the floor to update.
            floor_number (int): The new number of the floor.
            floor_name (str): The new name of the floor.
        
        Returns:
            Floor: The updated Floor object.
        """
        self.cursor.execute(
            "UPDATE floors SET level = %s, name = %s WHERE id = %s",
            (floor_number, floor_name, floor_id)
        )
        self.connection.commit()

        # Retrieve the updated floor
        self.cursor.execute("SELECT * FROM floors WHERE id = %s", (floor_id,))
        row = self.cursor.fetchone()

        if row:
            return Floor(**row)
        else:
            return None