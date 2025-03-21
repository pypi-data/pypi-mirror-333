import pandas as pd
import time
import logging
from pydbmanager.connection import DatabaseConnection
from pydbmanager.utils import execute_with_retry

class DatabaseOperations:
    """Handles database queries and operations."""

    def __init__(self):
        self.db = DatabaseConnection()
        self.conn = self.db.create_connection()

    def query_data(self, query: str, batch_size: int = None):
        """Executes a SELECT query and returns results as a DataFrame."""
        self.db.check_connection()

        if self.conn is None:
            logging.error("No active database connection.")
            return None

        start_time = time.time()
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)

            if batch_size:
                rows = []
                while True:
                    batch = cursor.fetchmany(batch_size)
                    if not batch:
                        break
                    rows.extend(batch)
            else:
                rows = cursor.fetchall()

            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame.from_records(rows, columns=columns)

            logging.info(f"Query executed in {time.time() - start_time:.4f} seconds")
            return df
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()

    def execute_query(self, query: str):
        """Executes an INSERT, UPDATE, or DELETE query."""
        return execute_with_retry(lambda: self._execute_query(query))

    def _execute_query(self, query: str) -> bool:
        self.db.check_connection()

        if self.conn is None:
            logging.error("No active database connection.")
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            logging.info("Query executed successfully!")
            return True
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            return False
        finally:
            cursor.close()

    def close(self):
        """Closes the database connection."""
        self.db.close_connection()
