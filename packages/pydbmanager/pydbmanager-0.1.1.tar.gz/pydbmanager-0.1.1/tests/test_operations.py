import unittest
from pydbmanager.operations import DatabaseOperations

class TestDatabaseOperations(unittest.TestCase):
    """Unit test for database operations (CRUD)."""

    def setUp(self):
        """Initialize database operations before each test."""
        self.db_ops = DatabaseOperations()

    def test_insert_data(self):
        """Test inserting a new user record."""
        query = """
        INSERT INTO users (name, email, age, gender, phone_number, address, city, country)
        VALUES ('Test User', 'test.user@example.com', 30, 'Male', '123-456-7890', '123 Test St', 'TestCity', 'TestCountry')
        """
        result = self.db_ops.execute_query(query)
        self.assertTrue(result, "Failed to insert data.")

    def test_fetch_data(self):
        """Test retrieving data from the database."""
        df = self.db_ops.query_data("SELECT * FROM users", batch_size=5)
        self.assertFalse(df.empty, "Query returned an empty DataFrame.")

    def test_update_data(self):
        """Test updating a record in the database."""
        query = """
        UPDATE users SET name = 'Updated Test User'
        WHERE email = 'test.user@example.com'
        """
        result = self.db_ops.execute_query(query)
        self.assertTrue(result, "Failed to update data.")

    def test_delete_data(self):
        """Test deleting a record from the database."""
        query = """
        DELETE FROM users WHERE email = 'test.user@example.com'
        """
        result = self.db_ops.execute_query(query)
        self.assertTrue(result, "Failed to delete data.")

    def tearDown(self):
        """Clean up database connection after tests."""
        self.db_ops.close()

if __name__ == "__main__":
    unittest.main()
    
# The test cases are designed to cover the basic CRUD operations (Create, Read, Update, Delete) on a sample "users" table. The tests are run in the following order:
#
# test_insert_data: Inserts a new user record into the database.        

# test_fetch_data: Retrieves all user records from the database in batches of 5.

# test_update_data: Updates the name of the user with the email '

# test_delete_data: Deletes the user record with the email column'

# The tearDown method is used to close the database connection after all tests have been executed. This ensures that the resources are properly released and the connection is closed.
