import unittest
from pydbmanager.connection import DatabaseConnection

class TestDatabaseConnection(unittest.TestCase):
    """Unit test for database connection"""

    def setUp(self):
        """Initialize database connection before each test"""
        self.db = DatabaseConnection()

    def test_create_connection(self):
        """Test if connection is established successfully."""
        conn = self.db.create_connection()
        self.assertIsNotNone(conn, "Failed to establish database connection.")

    def test_check_connection(self):
        """Test if the connection health check works"""
        self.db.check_connection()
        self.assertIsNotNone(self.db.conn, "Connection was not re-established.")

    def test_close_connection(self):
        """Test if the connection closes properly"""
        self.db.close_connection()
        self.assertIsNone(self.db.conn, "Database connection should be None after closing.")

if __name__ == "__main__":
    unittest.main()
