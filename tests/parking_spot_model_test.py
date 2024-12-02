import unittest
from unittest.mock import patch, MagicMock
from app.models.parking_spot_model import ParkingSpotModel
from app.utils.types.models.parkingSpot import ParkingSpot


class TestParkingSpotModel(unittest.TestCase):

    @patch('app.models.parking_spot_model.get_db_connection')
    def setUp(self, mock_get_db_connection):
        # Mock the database connection and cursor
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        mock_get_db_connection.return_value = (self.mock_connection, self.mock_cursor)
        
        # Initialize the model with the mocked database connection
        self.parking_spot_model = ParkingSpotModel()
        self.parking_spot_model.connection = self.mock_connection
        self.parking_spot_model.cursor = self.mock_cursor

    def test_get_parking_spots(self):
        # Mock the data returned from the DB
        self.mock_cursor.fetchall.return_value = [
            {'id': 1, 'floor_id': 1, 'spot_number': 'A1', 'created_at': '2024-01-01', 'updated_at': '2024-01-01'},
            {'id': 2, 'floor_id': 1, 'spot_number': 'A2', 'created_at': '2024-01-01', 'updated_at': '2024-01-01'}
        ]

        # Call the method
        parking_spots = self.parking_spot_model.get_parking_spots()

        # Verify that the database query was called
        self.mock_cursor.execute.assert_called_with("SELECT * FROM parking_spots")
        
        # Verify that the returned result is a list of ParkingSpot objects
        self.assertEqual(len(parking_spots), 2)
        self.assertIsInstance(parking_spots[0], ParkingSpot)
        self.assertEqual(parking_spots[0].spot_number, 'A1')
        
    def test_create_parking_spot(self):
        # Mock the data returned after insertion
        self.mock_cursor.fetchone.return_value = {'id': 1, 'floor_id': 1, 'spot_number': 'A1', 'created_at': '2024-01-01', 'updated_at': '2024-01-01'}

        # Call the method to create a parking spot
        parking_spot = self.parking_spot_model.create_parking_spot(1, 'A1')

        # Verify that the insert query was executed
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO parking_spots (floor_id, spot_number) VALUES (%s, %s)",
            (1, 'A1')
        )

        # Verify the returned ParkingSpot object
        self.assertEqual(parking_spot.spot_number, 'A1')

    def test_update_parking_spot(self):
        # Mock the data returned after the update
        self.mock_cursor.fetchone.return_value = {'id': 1, 'floor_id': 1, 'spot_number': 'A1', 'created_at': '2024-01-01', 'updated_at': '2024-01-01'}

        # Call the method to update a parking spot
        parking_spot = self.parking_spot_model.update_parking_spot(1, 1, 'A1')

        # Verify that the update query was executed
        self.mock_cursor.execute.assert_any_call(
            "UPDATE parking_spots SET floor_id = %s, spot_number = %s WHERE id = %s",
            (1, 'A1', 1)
        )

        # Verify the returned ParkingSpot object
        self.assertEqual(parking_spot.spot_number, 'A1')

    def test_delete_parking_spot(self):
        # Mock the result of the delete operation
        self.mock_cursor.rowcount = 1  # Simulate a successful delete

        # Call the method to delete a parking spot
        result = self.parking_spot_model.delete_parking_spot(1)

        # Verify that the delete query was executed
        self.mock_cursor.execute.assert_any_call("DELETE FROM parking_spots WHERE id = %s", (1,))
        
        # Verify that the method returns True for a successful deletion
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
