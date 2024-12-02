import unittest
from unittest.mock import MagicMock, patch
from app.models.floor_model import FloorModel
from app.utils.types.models.floor import Floor

class TestFloorModel(unittest.TestCase):

    @patch('app.models.floor_model.get_db_connection')
    def setUp(self, mock_get_db_connection):
        # Mock the database connection and cursor
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        
        mock_get_db_connection.return_value = (self.mock_connection, self.mock_cursor)
        
        # Initialize the FloorModel with the mocked DB connection and cursor
        self.floor_model = FloorModel()

    def test_get_floors(self):
        # Prepare mock data
        self.mock_cursor.fetchall.return_value = [
            {'id': 1, 'name': 'Ground Floor', 'level': 0, 'created_at': '2024-01-01', 'updated_at': '2024-01-01'},
            {'id': 2, 'name': 'First Floor', 'level': 1, 'created_at': '2024-01-01', 'updated_at': '2024-01-01'}
        ]
        
        # Call the method
        floors = self.floor_model.get_floors()
        
        # Verify the interaction with the database and the result
        self.mock_cursor.execute.assert_called_with("SELECT * FROM floors")
        self.assertEqual(len(floors), 2)
        self.assertIsInstance(floors[0], Floor)
        self.assertEqual(floors[0].name, 'Ground Floor')

    def test_get_floor_by_id_found(self):
        # Prepare mock data
        self.mock_cursor.fetchone.return_value = {'id': 1, 'name': 'Ground Floor', 'level': 0, 'created_at': '2024-01-01', 'updated_at': '2024-01-01'}
        
        # Call the method
        floor = self.floor_model.get_floor_by_id(1)
        
        # Verify the interaction with the database and the result
        self.mock_cursor.execute.assert_called_with("SELECT * FROM floors WHERE id = %s", (1,))
        self.assertIsInstance(floor, Floor)
        self.assertEqual(floor.name, 'Ground Floor')

    def test_get_floor_by_id_not_found(self):
        # Prepare mock data
        self.mock_cursor.fetchone.return_value = None
        
        # Call the method
        floor = self.floor_model.get_floor_by_id(1)
        
        # Verify the interaction with the database and the result
        self.mock_cursor.execute.assert_called_with("SELECT * FROM floors WHERE id = %s", (1,))
        self.assertIsNone(floor)

    def test_create_floor_success(self):
        # Prepare mock data for the SELECT query (simulating a newly created floor)
        self.mock_cursor.fetchone.return_value = {'id': 1, 'name': 'Ground Floor', 'level': 0, 'created_at': '2024-01-01', 'updated_at': '2024-01-01'}
        
        # Call the method to create a new floor
        floor = self.floor_model.create_floor(0, 'Ground Floor')
        
        # Verify that the INSERT query was called
        self.mock_cursor.execute.assert_any_call("INSERT INTO floors (level, name) VALUES (%s, %s)", (0, 'Ground Floor'))
        
        # Verify that the SELECT query was called to retrieve the created floor
        self.mock_cursor.execute.assert_any_call("SELECT * FROM floors WHERE level = %s", (0,))
        
        # Verify the result (check that the floor's name is 'Ground Floor')
        self.assertEqual(floor.name, 'Ground Floor')


    def test_create_floor_failure(self):
        # Simulate failure by returning None when fetching the floor
        self.mock_cursor.fetchone.return_value = None
        
        # Call the method
        floor = self.floor_model.create_floor(0, 'Ground Floor')
        
        # Verify the interaction with the database and the result
        self.assertIsNone(floor)

    def test_delete_floor_success(self):
        # Simulate successful deletion
        self.mock_cursor.rowcount = 1
        
        # Call the method
        result = self.floor_model.delete_floor(1)
        
        # Verify the interaction with the database and the result
        self.mock_cursor.execute.assert_called_with("DELETE FROM floors WHERE id = %s", (1,))
        self.assertTrue(result)

    def test_delete_floor_failure(self):
        # Simulate failure by setting rowcount to 0
        self.mock_cursor.rowcount = 0
        
        # Call the method
        result = self.floor_model.delete_floor(1)
        
        # Verify the interaction with the database and the result
        self.mock_cursor.execute.assert_called_with("DELETE FROM floors WHERE id = %s", (1,))
        self.assertFalse(result)

    def test_update_floor_success(self):
        # Prepare mock data for the SELECT query
        self.mock_cursor.fetchone.return_value = {'id': 1, 'name': 'First Floor Updated', 'level': 1, 'created_at': '2024-01-01', 'updated_at': '2024-01-01'}
        
        # Call the method
        floor = self.floor_model.update_floor(1, 1, 'First Floor Updated')
        
        # Verify the interaction with the database and the result
        self.mock_cursor.execute.assert_any_call("UPDATE floors SET level = %s, name = %s WHERE id = %s", (1, 'First Floor Updated', 1))
        self.mock_cursor.execute.assert_any_call("SELECT * FROM floors WHERE id = %s", (1,))
        
        # Verify the result
        self.assertEqual(floor.name, 'First Floor Updated')


    def test_update_floor_failure(self):
        # Simulate failure by returning None when fetching the updated floor
        self.mock_cursor.fetchone.return_value = None
        
        # Call the method
        floor = self.floor_model.update_floor(1, 1, 'First Floor Updated')
        
        # Verify the interaction with the database and the result
        self.assertIsNone(floor)


if __name__ == '__main__':
    unittest.main()
