import os
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

class Config:
    """Configuration class for database connection parameters."""

    SERVER = os.getenv("DB_SERVER")
    DATABASE = os.getenv("DB_DATABASE")
    USERNAME = os.getenv("DB_USERNAME")
    PASSWORD = os.getenv("DB_PASSWORD")
    DRIVER = os.getenv("DB_DRIVER", "{ODBC Driver 17 for SQL Server}")

    @staticmethod
    def validate():
        """Ensures all required configurations are provided."""
        missing = [key for key in ["SERVER", "DATABASE", "USERNAME", "PASSWORD"] if not getattr(Config, key)]
        if missing:
            raise ValueError(f"Missing required configuration values : {', '.join(missing)}")
