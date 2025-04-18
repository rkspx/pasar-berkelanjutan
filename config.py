import json
import os
import pathlib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment
FLASK_ENV = os.getenv("FLASK_ENV", "development")

# Load configuration once at startup
CONFIG_FILE = "app_config.json"

# Default configuration
DEFAULT_CONFIG = {
    "port": int(os.getenv("PORT", 5000)),  # Default Flask port
    "flask_secret_key": os.getenv("FLASK_SECRET_KEY", "pasar_berkelanjutan_secret_key"),
    "db_engine": os.getenv("DB_ENGINE", "sqlite" if FLASK_ENV in ["development", "testing"] else "postgresql"),
    "db_connection_string": ""
}

# Set default database connection string based on engine
if DEFAULT_CONFIG["db_engine"] == "sqlite":
    # SQLite for development and testing
    db_path = os.getenv("SQLITE_PATH", "sqlite:///pasar_berkelanjutan.db")
    if not db_path.startswith("sqlite:///"):
        db_path = f"sqlite:///{db_path}"
    DEFAULT_CONFIG["db_connection_string"] = db_path
else:
    # PostgreSQL for production
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "pasar_berkelanjutan")
    DEFAULT_CONFIG["db_connection_string"] = f"{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Load configuration from file if it exists
if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, 'r') as f:
            file_config = json.load(f)
            # Update default config with file config
            for key, value in file_config.items():
                DEFAULT_CONFIG[key] = value
    except (json.JSONDecodeError, IOError):
        # If there's an error reading the file, use default config
        pass

# Create a static CONFIG object that will be used throughout the application
CONFIG = DEFAULT_CONFIG.copy()

def get_port():
    """Get the configured port number"""
    return CONFIG["port"]

def get_db_uri():
    """Get the SQLAlchemy database URI"""
    db_engine = CONFIG["db_engine"]
    connection_string = CONFIG["db_connection_string"]
    
    # SQLite connection strings already include the protocol
    if db_engine == "sqlite":
        return connection_string
    
    # For other database engines, add the protocol
    if db_engine == "postgresql":
        return f"postgresql://{connection_string}"
    elif db_engine == "mysql":
        return f"mysql+pymysql://{connection_string}"
    elif db_engine == "oracle":
        return f"oracle+cx_oracle://{connection_string}"
    elif db_engine == "mssql":
        return f"mssql+pyodbc://{connection_string}"
    else:
        # Default to PostgreSQL if engine is unknown
        return f"postgresql://{connection_string}"