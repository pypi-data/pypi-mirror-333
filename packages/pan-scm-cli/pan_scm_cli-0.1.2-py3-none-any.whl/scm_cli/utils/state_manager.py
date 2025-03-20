"""State management for the SCM CLI application.

This module provides a centralized state management system that persists
CLI state across sessions using SQLite.
"""

import json
import logging
import sqlite3
from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime
from typing import Any, Dict, Optional, Set, TypeVar, cast, Type

from .db_utils import get_db_path, ensure_connection

# Use child logger from the root logger
logger = logging.getLogger("scm_cli.utils.state_manager")

# Type for serializable values
T = TypeVar('T')

# Table names
STATE_TABLE = "cli_state"
CACHE_TABLE = "cli_cache"
CONFIG_TABLE = "cli_config"


@dataclass
class StateEntry:
    """Data class for a state entry."""
    key: str
    value: str  # JSON serialized value
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CacheEntry:
    """Data class for a cache entry."""
    key: str
    value: str  # JSON serialized value
    ttl: int = 3600  # Time to live in seconds (default: 1 hour)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class StateManager:
    """Manages state persistence for the SCM CLI.
    
    This class provides:
    1. State persistence across CLI sessions
    2. Efficient caching of API responses and other data
    3. User configuration storage
    """
    
    def __init__(self, db_path: Optional[str] = None) -> None:
        """Initialize the state manager.
        
        Args:
            db_path: Optional path to the SQLite database file. If not provided,
                    uses the default path in the user data directory.
        """
        # If path is provided, use it directly, otherwise get the default path
        self.db_path = db_path if db_path else get_db_path()
        logger.debug(f"Using state database at: {self.db_path}")
        self._init_db()
    
    @ensure_connection
    def _init_db(self, conn=None) -> None:
        """Initialize the database with required tables.
        
        Args:
            conn: Optional database connection (provided by ensure_connection decorator)
        """
        logger.debug(f"Initializing state database at {self.db_path}")
        cursor = conn.cursor()
        
        # Create state table
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {STATE_TABLE} (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TEXT
        )
        """)
        
        # Create cache table with TTL support
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {CACHE_TABLE} (
            key TEXT PRIMARY KEY,
            value TEXT,
            ttl INTEGER,
            created_at TEXT
        )
        """)
        
        # Create config table
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {CONFIG_TABLE} (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TEXT
        )
        """)
    
    @ensure_connection
    def set_state(self, key: str, value: Any, conn=None) -> None:
        """Set a state value.
        
        Args:
            key: State key
            value: Value to store (must be JSON serializable)
            conn: Optional database connection (provided by ensure_connection decorator)
        """
        logger.debug(f"Setting state: {key}")
        serialized_value = json.dumps(value)
        updated_at = datetime.now().isoformat()
        
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT OR REPLACE INTO {STATE_TABLE} (key, value, updated_at) VALUES (?, ?, ?)",
            (key, serialized_value, updated_at)
        )
    
    @ensure_connection
    def get_state(self, key: str, default: Optional[T] = None, conn=None) -> Optional[T]:
        """Get a state value.
        
        Args:
            key: State key
            default: Default value if key doesn't exist
            conn: Optional database connection (provided by ensure_connection decorator)
            
        Returns:
            The stored value or default
        """
        logger.debug(f"Getting state: {key}")
        cursor = conn.cursor()
        cursor.execute(f"SELECT value FROM {STATE_TABLE} WHERE key = ?", (key,))
        row = cursor.fetchone()
        
        if row:
            try:
                return cast(T, json.loads(row[0]))
            except json.JSONDecodeError:
                logger.error(f"Failed to decode state value for key: {key}")
                return default
        
        return default
    
    @ensure_connection
    def delete_state(self, key: str, conn=None) -> bool:
        """Delete a state value.
        
        Args:
            key: State key
            conn: Optional database connection (provided by ensure_connection decorator)
            
        Returns:
            True if the key was deleted, False otherwise
        """
        logger.debug(f"Deleting state: {key}")
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {STATE_TABLE} WHERE key = ?", (key,))
        return cursor.rowcount > 0
    
    @ensure_connection
    def set_cache(self, key: str, value: Any, ttl: int = 3600, conn=None) -> None:
        """Set a cached value with TTL.
        
        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
            ttl: Time-to-live in seconds (default: 1 hour)
            conn: Optional database connection (provided by ensure_connection decorator)
        """
        logger.debug(f"Setting cache: {key} (TTL: {ttl}s)")
        serialized_value = json.dumps(value)
        created_at = datetime.now().isoformat()
        
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT OR REPLACE INTO {CACHE_TABLE} (key, value, ttl, created_at) VALUES (?, ?, ?, ?)",
            (key, serialized_value, ttl, created_at)
        )
    
    @ensure_connection
    def get_cache(self, key: str, default: Optional[T] = None, conn=None) -> Optional[T]:
        """Get a cached value (respecting TTL).
        
        Args:
            key: Cache key
            default: Default value if cache miss or expired
            conn: Optional database connection (provided by ensure_connection decorator)
            
        Returns:
            The cached value or default
        """
        logger.debug(f"Getting cache: {key}")
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT value, ttl, created_at FROM {CACHE_TABLE} WHERE key = ?", 
            (key,)
        )
        row = cursor.fetchone()
        
        if not row:
            return default
        
        value, ttl, created_at = row
        
        # Check if cache is expired
        created = datetime.fromisoformat(created_at)
        now = datetime.now()
        elapsed_seconds = (now - created).total_seconds()
        
        if elapsed_seconds > ttl:
            logger.debug(f"Cache expired for key: {key}")
            self.delete_cache(key)
            return default
        
        try:
            return cast(T, json.loads(value))
        except json.JSONDecodeError:
            logger.error(f"Failed to decode cached value for key: {key}")
            return default
    
    @ensure_connection
    def delete_cache(self, key: str, conn=None) -> bool:
        """Delete a cached value.
        
        Args:
            key: Cache key
            conn: Optional database connection (provided by ensure_connection decorator)
            
        Returns:
            True if the key was deleted, False otherwise
        """
        logger.debug(f"Deleting cache: {key}")
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {CACHE_TABLE} WHERE key = ?", (key,))
        return cursor.rowcount > 0
    
    @ensure_connection
    def clear_expired_cache(self, conn=None) -> int:
        """Clear all expired cache entries.
        
        Args:
            conn: Optional database connection (provided by ensure_connection decorator)
            
        Returns:
            Number of entries cleared
        """
        logger.debug("Clearing expired cache entries")
        now = datetime.now().isoformat()
        
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {CACHE_TABLE} 
            WHERE datetime(created_at) < datetime(?, -(ttl || ' seconds'))
            """, 
            (now,)
        )
        return cursor.rowcount
    
    @ensure_connection
    def set_config(self, key: str, value: Any, conn=None) -> None:
        """Set a user configuration value.
        
        Args:
            key: Config key
            value: Value to store (must be JSON serializable)
            conn: Optional database connection (provided by ensure_connection decorator)
        """
        logger.debug(f"Setting config: {key}")
        serialized_value = json.dumps(value)
        updated_at = datetime.now().isoformat()
        
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT OR REPLACE INTO {CONFIG_TABLE} (key, value, updated_at) VALUES (?, ?, ?)",
            (key, serialized_value, updated_at)
        )
    
    @ensure_connection
    def get_config(self, key: str, default: Optional[T] = None, conn=None) -> Optional[T]:
        """Get a user configuration value.
        
        Args:
            key: Config key
            default: Default value if key doesn't exist
            conn: Optional database connection (provided by ensure_connection decorator)
            
        Returns:
            The stored value or default
        """
        logger.debug(f"Getting config: {key}")
        cursor = conn.cursor()
        cursor.execute(f"SELECT value FROM {CONFIG_TABLE} WHERE key = ?", (key,))
        row = cursor.fetchone()
        
        if row:
            try:
                return cast(T, json.loads(row[0]))
            except json.JSONDecodeError:
                logger.error(f"Failed to decode config value for key: {key}")
                return default
        
        return default
    
    @ensure_connection
    def get_all_config(self, conn=None) -> Dict[str, Any]:
        """Get all user configuration values.
        
        Args:
            conn: Optional database connection (provided by ensure_connection decorator)
            
        Returns:
            Dictionary of all configuration keys and values
        """
        logger.debug("Getting all config values")
        result = {}
        
        cursor = conn.cursor()
        cursor.execute(f"SELECT key, value FROM {CONFIG_TABLE}")
        
        for key, value in cursor.fetchall():
            try:
                result[key] = json.loads(value)
            except json.JSONDecodeError:
                logger.error(f"Failed to decode config value for key: {key}")
                result[key] = None
        
        return result


class SerializableState:
    """Base class for state objects that can be serialized/deserialized.
    
    This class provides methods to convert dataclasses to/from
    dictionaries for JSON serialization.
    """
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create an instance from a dictionary.
        
        Args:
            data: Dictionary with state data
            
        Returns:
            New instance with the loaded state
        """
        return cls(**data)  # type: ignore
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert instance to a dictionary.
        
        Returns:
            Dictionary representation of the state
        """
        # Check if this is a dataclass instance using is_dataclass
        if is_dataclass(self):
            # Safe to use asdict with dataclass instances
            return asdict(self)
        else:
            # Fallback implementation for non-dataclass instances
            return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
    
    @classmethod
    def load(cls: Type[T], state_manager: StateManager, key: str, default: Optional[T] = None) -> T:
        """Load instance from state store.
        
        Args:
            state_manager: StateManager instance
            key: State key
            default: Default instance if key doesn't exist
            
        Returns:
            Loaded instance or default
        """
        data = state_manager.get_state(key)
        if data:
            return cls.from_dict(data)
        return default or cls()  # type: ignore
    
    def save(self, state_manager: StateManager, key: str) -> None:
        """Save instance to state store.
        
        Args:
            state_manager: StateManager instance
            key: State key
        """
        state_manager.set_state(key, self.to_dict())


@dataclass
class CLIState(SerializableState):
    """Persistent state for the SCM CLI.
    
    This dataclass represents the current CLI state and handles
    persistence across CLI sessions.
    """
    
    # User session state
    config_mode: bool = False
    current_folder: Optional[str] = None
    client_id: Optional[str] = None
    username: Optional[str] = None
    
    # Caches for autocompletion
    known_folders: Set[str] = field(default_factory=set)
    known_address_objects: Dict[str, Set[str]] = field(default_factory=dict)
    
    # Reference fields (not persisted)
    _state_manager: Optional[StateManager] = field(default=None, repr=False, compare=False)
    
    @classmethod
    def load_or_create(cls, state_manager: StateManager) -> 'CLIState':
        """Load the CLI state from persistent storage or create a new one.
        
        Args:
            state_manager: StateManager instance
            
        Returns:
            CLIState instance
        """
        state = cls.load(state_manager, 'cli_state')
        state._state_manager = state_manager
        return state
    
    def save_state(self) -> None:
        """Save the current CLI state to persistent storage."""
        if self._state_manager:
            self.save(self._state_manager, 'cli_state')
            
    # Helper methods for state transitions
    
    def enter_config_mode(self) -> None:
        """Enter configuration mode."""
        self.config_mode = True
        self.save_state()
    
    def exit_config_mode(self) -> None:
        """Exit configuration mode."""
        self.config_mode = False
        self.save_state()
    
    def set_folder(self, folder: str) -> None:
        """Set the current folder context.
        
        Args:
            folder: Folder name
        """
        self.current_folder = folder
        
        # Add to known folders for autocompletion
        if folder:
            self.known_folders.add(folder)
        
        self.save_state()
    
    def exit_folder(self) -> None:
        """Exit the current folder context."""
        self.current_folder = None
        self.save_state()
    
    def set_user_info(self, client_id: str, username: Optional[str] = None) -> None:
        """Set user identification information.
        
        Args:
            client_id: Client ID from OAuth credentials
            username: Username (optional, extracted from client_id if not provided)
        """
        self.client_id = client_id
        
        if username:
            self.username = username
        elif client_id:
            # Extract username from client_id if not provided
            import re
            match = re.match(r"^([^@]+)@?.*$", client_id)
            if match:
                self.username = match.group(1)
            else:
                self.username = client_id
                
        self.save_state()
    
    def add_known_address_object(self, folder: str, name: str) -> None:
        """Add an address object to the known objects for autocompletion.
        
        Args:
            folder: Folder containing the object
            name: Object name
        """
        if folder not in self.known_address_objects:
            self.known_address_objects[folder] = set()
        
        self.known_address_objects[folder].add(name)
        self.save_state()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary for serialization.
        
        Special handling for set and nested set types.
        
        Returns:
            Dictionary representation
        """
        # Make a copy of our dict and manually convert sets
        # This is safer than using asdict directly
        data: Dict[str, Any] = {'config_mode': self.config_mode, 'current_folder': self.current_folder,
                                'client_id': self.client_id, 'username': self.username,
                                'known_folders': list(self.known_folders)}
        
        # Copy basic fields

        # Convert sets to lists for JSON serialization

        # Convert nested sets to lists
        known_objects = {}
        for folder, objects in self.known_address_objects.items():
            known_objects[folder] = list(objects)
        data['known_address_objects'] = known_objects
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CLIState':
        """Create an instance from a dictionary.
        
        Args:
            data: Dictionary with state data
            
        Returns:
            New CLIState instance
        """
        # Convert lists back to sets
        if 'known_folders' in data:
            data['known_folders'] = set(data['known_folders'])
        
        # Convert nested lists back to sets
        if 'known_address_objects' in data:
            known_objects = {}
            for folder, objects in data['known_address_objects'].items():
                known_objects[folder] = set(objects)
            data['known_address_objects'] = known_objects
        
        # Remove any reference fields that shouldn't be in initialization
        data.pop('_state_manager', None)
        
        return cls(**data)


def get_cache_key(endpoint: str, params: Dict[str, Any]) -> str:
    """Generate a unique cache key for an API request.

    Args:
        endpoint: API endpoint (e.g., 'address/list')
        params: Request parameters

    Returns:
        Unique cache key
    """
    # Normalize params to ensure consistent key generation
    param_str = json.dumps(params, sort_keys=True)
    return f"api:{endpoint}:{param_str}"


class APICacheManager:
    """Manages caching of API responses.
    
    This class provides methods to cache and retrieve API responses,
    with support for TTL-based expiration.
    """
    
    def __init__(self, state_manager: StateManager) -> None:
        """Initialize the API cache manager.
        
        Args:
            state_manager: StateManager instance
        """
        self.state_manager = state_manager

    def get_cached_response(self, endpoint: str, params: Dict[str, Any], default: Optional[T] = None) -> Optional[T]:
        """Get a cached API response.
        
        Args:
            endpoint: API endpoint
            params: Request parameters
            default: Default value if cache miss
            
        Returns:
            Cached response or default
        """
        cache_key = get_cache_key(endpoint, params)
        return self.state_manager.get_cache(cache_key, default)
    
    def cache_response(self, endpoint: str, params: Dict[str, Any], response: Any, ttl: int = 300) -> None:
        """Cache an API response.
        
        Args:
            endpoint: API endpoint
            params: Request parameters
            response: API response to cache
            ttl: Time-to-live in seconds (default: 5 minutes)
        """
        cache_key = get_cache_key(endpoint, params)
        self.state_manager.set_cache(cache_key, response, ttl)
    
    def invalidate_cache(self, endpoint: str, params: Dict[str, Any]) -> None:
        """Invalidate a cached API response.
        
        Args:
            endpoint: API endpoint
            params: Request parameters
        """
        cache_key = get_cache_key(endpoint, params)
        self.state_manager.delete_cache(cache_key)
    
    def invalidate_by_prefix(self, prefix: str) -> int | None | Any:
        """Invalidate all cache entries with a specific prefix.
        
        Args:
            prefix: Cache key prefix
            
        Returns:
            Number of cache entries invalidated
        """
        # We need to use the state manager's connection handling
        # Since this requires multiple operations, we'll use a single connection
        count = 0
        
        # Get keys with matching prefix
        conn = sqlite3.connect(self.state_manager.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT key FROM {CACHE_TABLE} WHERE key LIKE ?", (f"{prefix}%",))
            keys = [row[0] for row in cursor.fetchall()]
            
            # Delete each key
            for key in keys:
                cursor.execute(f"DELETE FROM {CACHE_TABLE} WHERE key = ?", (key,))
                count += 1
            
            conn.commit()
        finally:
            conn.close()
        
        return count
    
    def clear_all_cache(self) -> int:
        """Clear all API cache entries.
        
        Returns:
            Number of cache entries cleared
        """
        # Clear all cache entries with prefix 'api:'
        return self.invalidate_by_prefix('api:')
    
    def get_cache_stats(self) -> dict[str, dict[Any, Any] | Any] | None:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        # Get statistics in a single connection
        conn = sqlite3.connect(self.state_manager.db_path)
        try:
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute(f"SELECT COUNT(*) FROM {CACHE_TABLE} WHERE key LIKE 'api:%'")
            total_count = cursor.fetchone()[0]
            
            # Get endpoint counts
            cursor.execute(f"""
            SELECT SUBSTR(key, 5, INSTR(key, ':', 5) - 5) as endpoint, 
                   COUNT(*) as count 
            FROM {CACHE_TABLE} 
            WHERE key LIKE 'api:%' 
            GROUP BY endpoint
            """)
            endpoint_counts = {row[0]: row[1] for row in cursor.fetchall()}
        finally:
            conn.close()
            
        return {
            'total_count': total_count,
            'endpoint_counts': endpoint_counts
        }