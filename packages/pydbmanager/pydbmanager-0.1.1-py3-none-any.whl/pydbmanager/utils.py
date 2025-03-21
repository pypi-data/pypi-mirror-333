import logging
import time
import pandas as pd
from functools import lru_cache

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def execute_with_retry(func, retries=3, delay=2):
    """Retries a function in case of failure."""
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            logging.warning(f"Retry {i+1}/{retries} failed: {e}")
            time.sleep(delay)
    logging.error("Function failed after maximum retries.")
    return False

@lru_cache(maxsize=100)
def cached_query(query_func):
    """Caches the result of a query to optimize performance."""
    return query_func()

def save_query_results(df: pd.DataFrame, file_path: str, file_type: str = "csv"):
    """Saves query results to CSV or JSON."""
    if file_type == "csv":
        df.to_csv(file_path, index=False)
    elif file_type == "json":
        df.to_json(file_path, orient="records")
    logging.info(f"Data saved to {file_path}")
