"""Database module for SCM CLI history."""

import datetime
import logging
from typing import List, Optional, Tuple

from .db_utils import get_db_path, ensure_connection

# Use child logger from the root logger
logger = logging.getLogger("scm_cli.utils.db")

# Table name constant
HISTORY_TABLE = "command_history"

class CLIHistoryDB:
    """Database for storing CLI command history."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        """Initialize the history database.
        
        Args:
            db_path: Optional path to the SQLite database file. If not provided,
                    uses the default path in the user data directory.
        """
        # If path is provided, use it directly, otherwise get the default path
        self.db_path = db_path if db_path else get_db_path()
        logger.debug(f"Using history database at: {self.db_path}")
        self._initialize_db()
        
    @ensure_connection
    def _initialize_db(self, conn=None) -> None:
        """Initialize the database with required tables.
        
        Args:
            conn: Optional database connection (provided by ensure_connection decorator)
        """
        cursor = conn.cursor()
        
        # Create command history table if it doesn't exist
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {HISTORY_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            command TEXT NOT NULL,
            response TEXT,
            folder TEXT,
            success INTEGER
        )
        ''')
        
    @ensure_connection
    def add_command(
        self, 
        command: str, 
        response: Optional[str] = None, 
        folder: Optional[str] = None,
        success: bool = True,
        conn=None
    ) -> int:
        """Add a command to the history.
        
        Args:
            command: The command that was executed
            response: The response from the command
            folder: The current folder context when the command was executed
            success: Whether the command executed successfully
            conn: Optional database connection (provided by ensure_connection decorator)
            
        Returns:
            The ID of the inserted record
        """
        cursor = conn.cursor()
        
        timestamp = datetime.datetime.now().isoformat()
        
        cursor.execute(
            f"INSERT INTO {HISTORY_TABLE} (timestamp, command, response, folder, success) VALUES (?, ?, ?, ?, ?)",
            (timestamp, command, response, folder, 1 if success else 0)
        )
        
        return cursor.lastrowid
        
    @ensure_connection
    def get_history(
        self, 
        limit: int = 50,
        page: int = 1,
        folder: Optional[str] = None,
        command_filter: Optional[str] = None,
        conn=None
    ) -> Tuple[List[Tuple[int, str, str, str, str, bool]], int]:
        """Get command history with pagination.
        
        Args:
            limit: Maximum number of records to return per page
            page: Page number (starting from 1)
            folder: Filter by folder context
            command_filter: Filter commands containing this string
            conn: Optional database connection (provided by ensure_connection decorator)
            
        Returns:
            Tuple of (history_items, total_count) where:
                - history_items: List of tuples (id, timestamp, command, response, folder, success)
                - total_count: Total number of matching records (ignoring pagination)
        """
        cursor = conn.cursor()
        
        # Base query for both count and data retrieval
        base_query = f"FROM {HISTORY_TABLE}"
        params = []
        
        where_clauses = []
        if folder:
            where_clauses.append("folder = ?")
            params.append(folder)
            
        if command_filter:
            where_clauses.append("command LIKE ?")
            params.append(f"%{command_filter}%")
            
        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)
        
        # Get total count
        count_query = f"SELECT COUNT(*) {base_query}"
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()[0]
        
        # Calculate offset
        offset = (page - 1) * limit
        
        # Get paginated data
        data_query = f"SELECT id, timestamp, command, response, folder, success {base_query} ORDER BY id DESC LIMIT ? OFFSET ?"
        cursor.execute(data_query, params + [limit, offset])
        
        results = [
            (
                row[0],                  # id
                row[1],                  # timestamp
                row[2],                  # command
                row[3] if row[3] else "", # response
                row[4] if row[4] else "", # folder
                bool(row[5])             # success
            )
            for row in cursor.fetchall()
        ]
        
        return results, total_count
        
    @ensure_connection
    def get_history_entry(self, entry_id: int, conn=None) -> Optional[Tuple[int, str, str, str, str, bool]]:
        """Get a specific history entry by ID.
        
        Args:
            entry_id: The ID of the history entry to retrieve
            conn: Optional database connection (provided by ensure_connection decorator)
            
        Returns:
            Tuple of (id, timestamp, command, response, folder, success) or None if not found
        """
        cursor = conn.cursor()
        
        cursor.execute(
            f"SELECT id, timestamp, command, response, folder, success FROM {HISTORY_TABLE} WHERE id = ?",
            (entry_id,)
        )
        
        row = cursor.fetchone()
        
        if not row:
            return None
            
        return (
            row[0],                  # id
            row[1],                  # timestamp
            row[2],                  # command
            row[3] if row[3] else "", # response
            row[4] if row[4] else "", # folder
            bool(row[5])             # success
        )
        
    @ensure_connection
    def clear_history(self, conn=None) -> None:
        """Clear all command history.
        
        Args:
            conn: Optional database connection (provided by ensure_connection decorator)
        """
        cursor = conn.cursor()
        
        cursor.execute(f"DELETE FROM {HISTORY_TABLE}")