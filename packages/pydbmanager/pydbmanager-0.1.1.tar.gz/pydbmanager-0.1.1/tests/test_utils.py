import unittest
import pandas as pd
from pydbmanager.utils import execute_with_retry, save_query_results

class TestUtils(unittest.TestCase):
    """Unit tests for utility functions."""

    def test_execute_with_retry(self):
        """Test retry mechanism."""
        def failing_function():
            raise Exception("Simulated failure")

        result = execute_with_retry(lambda: 1, retries=2)
        self.assertEqual(result, 1, "Failed to return correct value.")

    def test_save_query_results(self):
        """Test saving query results to a CSV file."""
        df = pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})
        save_query_results(df, "test_output.csv", "csv")

        with open("test_output.csv", "r") as file:
            content = file.read()
        self.assertIn("Alice", content, "CSV file did not save correctly.")

if __name__ == "__main__":
    unittest.main()
