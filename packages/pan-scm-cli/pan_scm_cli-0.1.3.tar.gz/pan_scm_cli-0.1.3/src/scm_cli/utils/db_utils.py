"""Common database utilities for SCM CLI."""

import logging
import os
import platform
import sqlite3
from typing import Optional

# Use child logger from the root logger
logger = logging.getLogger("scm_cli.utils.db_utils")

# Database directory and file constants
DEFAULT_DIR_NAME = ".scm_cli"
DEFAULT_DB_NAME = "scm_cli.db"

def get_user_data_dir() -> str:
    """Get the appropriate user data directory based on the platform.
    
    Returns:
        Path to the user data directory
    """
    system = platform.system()
    
    if system == "Windows":
        # On Windows, use AppData/Local
        base_dir = os.environ.get("LOCALAPPDATA")
        if not base_dir:
            # Fallback to user profile
            base_dir = os.environ.get("USERPROFILE")
            if not base_dir:
                base_dir = os.path.expanduser("~")
    else:
        # On Linux, macOS, etc., use ~/.scm_cli
        base_dir = os.path.expanduser("~")
    
    return os.path.join(base_dir, DEFAULT_DIR_NAME)

def get_db_path(db_name: Optional[str] = None) -> str:
    """Get the full path to a database file.
    
    Args:
        db_name: Optional database filename (default: scm_cli.db)
        
    Returns:
        Full path to the database file
    """
    data_dir = get_user_data_dir()
    db_name = db_name or DEFAULT_DB_NAME
    db_path = os.path.join(data_dir, db_name)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    return db_path

def ensure_connection(func):
    """Decorator to ensure a database connection is available.
    
    This decorator checks if a connection is passed as a keyword argument.
    If not, it creates a temporary connection for the duration of the function call.
    
    Args:
        func: Function to decorate
        
    Returns:
        Wrapped function that handles connections
    """
    def wrapper(*args, **kwargs):
        # Check if a connection was provided
        conn = kwargs.get('conn')
        should_close = False
        
        if conn is None:
            # Get the self argument (first positional argument)
            self_obj = args[0]
            # Create a new connection
            conn = sqlite3.connect(self_obj.db_path)
            kwargs['conn'] = conn
            should_close = True
        
        try:
            # Call the original function
            result = func(*args, **kwargs)
            
            # Commit if we created the connection
            if should_close:
                conn.commit()
                
            return result
        finally:
            # Close if we created the connection
            if should_close:
                conn.close()
                
    return wrapper