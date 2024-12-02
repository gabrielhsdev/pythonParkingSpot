import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from app.models.car_model import CarModel
from app.utils.types.models.car import Car

class TestCarModel(unittest.TestCase):
    @patch('app.models.car_model.get_db_connection')  # Mock the DB connection
    def setUp(self, mock_get_db_connection):
        # Mock the database connection and cursor
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()

        # Return the mock connection and cursor when the get_db_connection is called
        mock_get_db_connection.return_value = (self.mock_connection, self.mock_cursor)

        # Create an instance of the CarModel
        self.car_model = CarModel()

    def test_get_cars(self):
        # Mock the cursor's execute and fetchall methods
        self.mock_cursor.fetchall.return_value = [
            {'id': 1, 'license_plate': 'ABC123', 'parking_spot_id': 1, 'arrive_at': datetime.now(), 'leave_at': None, 'created_at': datetime.now()},
            {'id': 2, 'license_plate': 'XYZ456', 'parking_spot_id': 2, 'arrive_at': datetime.now(), 'leave_at': None, 'created_at': datetime.now()}
        ]

        # Call the method
        cars = self.car_model.get_cars()

        # Assert the correct Car objects are returned
        self.assertEqual(len(cars), 2)
        self.assertIsInstance(cars[0], Car)
        self.assertEqual(cars[0].license_plate, 'ABC123')

    def test_get_car_by_id(self):
        # Mock the cursor's execute and fetchone methods
        self.mock_cursor.fetchone.return_value = {
            'id': 1, 
            'license_plate': 'ABC123', 
            'parking_spot_id': 1, 
            'arrive_at': datetime.now(), 
            'leave_at': None, 
            'created_at': datetime.now()
        }

        # Call the method
        car = self.car_model.get_car_by_id(1)

        # Assert the correct Car object is returned
        self.assertIsInstance(car, Car)
        self.assertEqual(car.license_plate, 'ABC123')

    def test_get_car_by_id_not_found(self):
        # Mock the cursor's execute and fetchone methods
        self.mock_cursor.fetchone.return_value = None

        # Call the method
        car = self.car_model.get_car_by_id(999)
        car = None

        # Assert None is returned when the car is not found
        self.assertIsNone(car)

    def test_create_car(self):
        # Mock the cursor's execute and fetchone methods
        self.mock_cursor.fetchone.return_value = {
            'id': 1, 
            'license_plate': 'ABC123', 
            'parking_spot_id': 1, 
            'arrive_at': datetime.now(), 
            'leave_at': None, 
            'created_at': datetime.now()
        }

        # Call the method
        car = self.car_model.create_car('ABC123', 1)

        # Assert the correct Car object is returned
        self.assertIsInstance(car, Car)
        self.assertEqual(car.license_plate, 'ABC123')

    def test_update_car_leave_at(self):
        # Mock the cursor's execute and fetchone methods
        self.mock_cursor.fetchone.return_value = {
            'id': 1, 
            'license_plate': 'ABC123', 
            'parking_spot_id': 1, 
            'arrive_at': datetime.now(), 
            'leave_at': datetime.now(), 
            'created_at': datetime.now()
        }

        # Call the method
        car = self.car_model.update_car_leave_at(1)

        # Assert the correct Car object is returned
        self.assertIsInstance(car, Car)
        self.assertEqual(car.license_plate, 'ABC123')

    def test_update_car_spot(self):
        # Mock the cursor's execute and fetchone methods
        self.mock_cursor.fetchone.return_value = {
            'id': 1, 
            'license_plate': 'ABC123', 
            'parking_spot_id': 2, 
            'arrive_at': datetime.now(), 
            'leave_at': None, 
            'created_at': datetime.now()
        }

        # Call the method
        car = self.car_model.update_car_spot(1, 2)

        # Assert the correct Car object is returned
        self.assertIsInstance(car, Car)
        self.assertEqual(car.parking_spot_id, 2)


    def test_delete_car(self):
        # Mock the cursor's execute method and simulate successful deletion
        self.mock_cursor.rowcount = 1  # Simulate one row affected (successful deletion)

        # Call the method
        result = self.car_model.delete_car(1)

        # Assert the car was deleted
        self.assertTrue(result)

    def test_delete_car_not_found(self):
        # Mock the cursor's execute method and simulate no deletion
        self.mock_cursor.rowcount = 0  # Simulate no rows affected (deletion failed)

        # Call the method
        result = self.car_model.delete_car(999)

        # Assert the car was not deleted
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
