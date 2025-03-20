"""Address object command module for SCM CLI."""

import logging
import time
from typing import Dict, List, Optional, Any, Tuple

from rich.console import Console
from rich.table import Table
from rich.box import ROUNDED
from scm.client import ScmClient

from .models import (
    AddressObjectAPI,
    ValidationError,
    ResourceNotFoundError,
    APIError,
    SDK_TO_CLI_TYPE,
)

# Use child logger from the root logger
logger = logging.getLogger("scm_cli.cli.object.address_object")


def parse_quoted_value(args: List[str], start_index: int) -> Tuple[str, int]:
    """Parse a potentially quoted string value from command arguments.
    
    This helper function handles values that may be:
    - Unquoted: single argument with no special handling
    - Double quoted: wrapped in double quotes (") and may span multiple arguments
    - Single quoted: wrapped in single quotes (') and may span multiple arguments
    
    It also handles escaped quotes within the quoted strings.
    
    Args:
        args: List of command arguments
        start_index: The index of the first argument to process
        
    Returns:
        Tuple containing (parsed_value, end_index)
        - parsed_value: The processed string with quotes removed if applicable
        - end_index: The index of the last argument that was consumed
    """
    if start_index >= len(args):
        return "", start_index
        
    value = args[start_index]
    end_index = start_index
    quote_char = None
    
    # Detect quote type if present
    if value.startswith('"'):
        quote_char = '"'
    elif value.startswith("'"):
        quote_char = "'"
    
    # If no quotes or complete quotes in a single argument, handle simply
    if not quote_char or (value.startswith(quote_char) and value.endswith(quote_char) and len(value) > 1):
        # For single argument with quotes, just strip them
        if quote_char and value.startswith(quote_char) and value.endswith(quote_char):
            value = value[1:-1]
            
            # Unescape any escaped quotes
            if quote_char == '"':
                value = value.replace('\\"', '"')
            elif quote_char == "'":
                value = value.replace("\\'", "'")
                
        return value, end_index
    
    # Handle multipart quoted string (quotes that span multiple arguments)
    if quote_char:
        j = start_index + 1
        while j < len(args):
            # Add space and next part
            value += " " + args[j]
            
            # Check if this part ends with the closing quote
            # But make sure it's not an escaped quote (e.g., \")
            if args[j].endswith(quote_char) and not args[j].endswith(f"\\{quote_char}"):
                end_index = j
                break
            j += 1
            
        # Strip quotes from the final string if they're matching
        if value.startswith(quote_char) and value.endswith(quote_char):
            value = value[1:-1]  # Remove surrounding quotes
            
            # Unescape any escaped quotes in the content
            if quote_char == '"':
                value = value.replace('\\"', '"')
            elif quote_char == "'":
                value = value.replace("\\'", "'")
    
    return value, end_index


def parse_address_object_args(args: List[str]) -> Dict[str, Any]:
    """Parse the set address-object command with positional name and keyword arguments.

    This parser is designed to handle networking-style CLI commands like:
    set address-object test1 type ip-netmask value 1.1.1.1/32 description "Test desc" tags tag1,tag2

    It also supports partial updates (like PATCH) for existing objects:
    set address-object test1 description "Updated description"

    Args:
        args: List of argument strings

    Returns:
        Dictionary with parsed arguments and a 'partial_update' flag

    Raises:
        ValueError: If required arguments are missing or format is invalid
    """
    if len(args) < 1:  # Need at least the name as a positional argument
        raise ValueError("Missing required arguments: must at least specify object name")

    # Extract name (first argument) and handle potential quotes
    name, end_idx = parse_quoted_value(args, 0)
    
    # Setup parsed arguments with the name
    parsed_args = {
        "name": name,
        "partial_update": False
    }
    
    # Start processing from after the name
    i = end_idx + 1

    while i < len(args):
        # Get the keyword
        keyword = args[i].lower()
        i += 1

        # Check if we have a value for this keyword
        if i >= len(args):
            raise ValueError(f"Missing value for {keyword}")

        # Process based on keyword
        if keyword == "type":
            # Validate type (typically doesn't need quote handling)
            valid_types = ["ip-netmask", "ip-range", "fqdn"]
            if args[i] not in valid_types:
                valid_types_str = ", ".join(valid_types)
                raise ValueError(
                    f"Invalid address type: {args[i]}. Valid types are: {valid_types_str}"
                )
            parsed_args["type"] = args[i]
        elif keyword == "value":
            # Value might contain quotes (especially for FQDN)
            value, end_idx = parse_quoted_value(args, i)
            parsed_args["value"] = value
            i = end_idx  # Update index to end of processed value
        elif keyword == "description":
            # Description often contains spaces, so use our helper function
            value, end_idx = parse_quoted_value(args, i)
            parsed_args["description"] = value
            i = end_idx  # Update index to end of processed value
        elif keyword == "tags":
            # Parse comma-separated tags
            # First, handle quoted tag list (e.g., "tag1,tag2,tag3")
            value, end_idx = parse_quoted_value(args, i)
            # Then split the tags
            parsed_args["tag"] = [tag.strip() for tag in value.split(",")]
            i = end_idx  # Update index to end of processed value
        elif keyword == "name":
            # "name" keyword is now redundant since name is positional,
            # but we'll handle it for backward compatibility with warning
            value, end_idx = parse_quoted_value(args, i)
            # Log a warning about using deprecated 'name' keyword
            logger.warning("The 'name' keyword is deprecated. Object name should be provided as the first positional argument")
            # Only override if different (though this should be rare)
            if value != parsed_args["name"]:
                parsed_args["name"] = value
            i = end_idx
        else:
            raise ValueError(f"Unknown keyword: {keyword}")

        # Advance to next keyword
        i += 1

    # Check if this is a partial update (missing required fields)
    required_fields = ["name", "type", "value"]
    has_all_required = all(field in parsed_args for field in required_fields)

    if not has_all_required:
        # Mark as a partial update - we'll validate if the object exists later
        parsed_args["partial_update"] = True

    return parsed_args


def _get_address_value(address_obj: Any) -> str:
    """Extract the address value based on type.

    Args:
        address_obj: Address object (Pydantic model or dict)

    Returns:
        Address value as string
    """
    # Try attribute access first (Pydantic model)
    if hasattr(address_obj, "ip_netmask") and getattr(address_obj, "ip_netmask"):
        return getattr(address_obj, "ip_netmask")
    elif hasattr(address_obj, "ip_range") and getattr(address_obj, "ip_range"):
        return getattr(address_obj, "ip_range")
    elif hasattr(address_obj, "fqdn") and getattr(address_obj, "fqdn"):
        return getattr(address_obj, "fqdn")

    # Fall back to dictionary access
    if isinstance(address_obj, dict):
        if address_obj.get("ip_netmask"):
            return address_obj["ip_netmask"]
        elif address_obj.get("ip_range"):
            return address_obj["ip_range"]
        elif address_obj.get("fqdn"):
            return address_obj["fqdn"]

    return ""


def _get_address_type(address_obj: Any) -> str:
    """Get the address type and convert to CLI format.

    Args:
        address_obj: Address object (Pydantic model or dict)

    Returns:
        Address type in CLI format
    """
    # Determine type by checking which field has a value
    # For Pydantic models
    if hasattr(address_obj, "ip_netmask") and getattr(address_obj, "ip_netmask"):
        return "ip-netmask"
    elif hasattr(address_obj, "ip_range") and getattr(address_obj, "ip_range"):
        return "ip-range"
    elif hasattr(address_obj, "fqdn") and getattr(address_obj, "fqdn"):
        return "fqdn"

    # For dictionaries
    if isinstance(address_obj, dict):
        if address_obj.get("ip_netmask"):
            return "ip-netmask"
        elif address_obj.get("ip_range"):
            return "ip-range"
        elif address_obj.get("fqdn"):
            return "fqdn"

    # If we can't determine by field, try using the type attribute
    if hasattr(address_obj, "type"):
        addr_type = getattr(address_obj, "type")
        # If it's an enum, get the value
        if hasattr(addr_type, "value"):
            addr_type = addr_type.value
        return SDK_TO_CLI_TYPE.get(addr_type, addr_type)

    # Fall back to dictionary access
    if isinstance(address_obj, dict) and "type" in address_obj:
        return SDK_TO_CLI_TYPE.get(address_obj["type"], address_obj["type"])

    return ""


def _get_address_tags(address_obj: Any) -> str:
    """Get tags from address object.

    Args:
        address_obj: Address object (Pydantic model or dict)

    Returns:
        Comma-separated tags string
    """
    # Try attribute access first (Pydantic model)
    if hasattr(address_obj, "tag"):
        tags = getattr(address_obj, "tag") or []
        return ", ".join(tags)

    # Fall back to dictionary access
    if isinstance(address_obj, dict):
        tags = address_obj.get("tag", [])
        return ", ".join(tags)

    return ""


class AddressObjectCommands:
    """Address object commands for SCM CLI."""

    def __init__(self, console: Console, client: ScmClient, api_cache=None):
        """Initialize address object commands.

        Args:
            console: Rich console for output
            client: Initialized SCM client
            api_cache: Optional API cache manager
        """
        self.console = console
        self.client = client
        self.api_cache = api_cache
        self.api = AddressObjectAPI(client, api_cache)

    def set_address_object(self, folder: str, args: List[str]) -> None:
        """Set (create or update) an address object.

        Args:
            folder: Folder to set address object in
            args: Arguments for the address object
        """
        try:
            # Parse networking-style keyword arguments
            if len(args) < 2:  # Need at least "address-object" and object name
                self.console.print("Missing required arguments", style="red")
                self.console.print(
                    "Usage: set address-object <name> type <type> value <value> [description <text>] [tags <tag1,tag2,...>]"
                )
                return

            # Remove the first argument ('address-object') and process the rest
            object_args = args[1:]
            
            # Parse the arguments using the parser that handles positional name
            parsed_args = parse_address_object_args(object_args)

            # Extract values from the parsed arguments
            name = parsed_args["name"]
            is_partial_update = parsed_args.get("partial_update", False)

            # Start timer for overall performance
            time.time()

            # Enable debug mode - shows timing information
            debug_timing = True

            # Create timing log function
            def log_timing(operation: str, duration: float) -> None:
                """Log timing information if debug_timing is enabled."""
                if debug_timing:
                    self.console.print(
                        f"[dim]DEBUG: {operation} took {duration:.3f} seconds[/dim]",
                        style="dim",
                    )

            try:
                # First check if the object exists
                with self.console.status(
                    f"[bold yellow]Checking if address object '{name}' exists...[/bold yellow]"
                ):
                    check_start = time.time()
                    existing_object = self.api.get_object(folder, name)
                    check_end = time.time()
                    log_timing(f"Checking if object exists", check_end - check_start)

                # Handle partial update scenario
                if is_partial_update:
                    if not existing_object:
                        # Can't do a partial update on a non-existent object
                        self.console.print(
                            f"Error: Cannot perform partial update on a non-existent object: '{name}'",
                            style="red",
                        )
                        self.console.print(
                            "For a new object, you must specify all required fields: name, type, and value",
                            style="yellow",
                        )
                        return

                    self.console.print(
                        f"Performing partial update on existing object: '{name}'",
                        style="yellow",
                    )

                # Decision based on existence check
                if existing_object:
                    # Object exists, update it
                    self.console.print(
                        f"Found existing object: '{name}', will update", style="yellow"
                    )
                    with self.console.status(
                        f"[bold yellow]Updating address object '{name}'...[/bold yellow]"
                    ):
                        update_start = time.time()
                        address = self.api.update_object(folder, name, parsed_args)
                        update_end = time.time()
                        log_timing(
                            f"Updating object '{name}'", update_end - update_start
                        )

                    # Display the updated object in a table
                    self.console.print(
                        f"✅ - updated address-object {name}", style="green"
                    )
                    self._display_object_as_table(address)
                else:
                    # Object doesn't exist, create it
                    if is_partial_update:
                        # This shouldn't happen because we already checked above
                        self.console.print(
                            f"Error: Cannot create object with partial data. Must specify name, type, and value.",
                            style="red",
                        )
                        return

                    self.console.print(
                        f"No existing object found: '{name}', will create",
                        style="yellow",
                    )
                    with self.console.status(
                        f"[bold yellow]Creating address object '{name}'...[/bold yellow]"
                    ):
                        create_start = time.time()
                        address = self.api.create_object(folder, parsed_args)
                        create_end = time.time()
                        log_timing(
                            f"Creating object '{name}'", create_end - create_start
                        )

                    # Display the created object in a table
                    self.console.print(
                        f"✅ - created address-object {name}", style="green"
                    )
                    self._display_object_as_table(address)

            except ValidationError as e:
                if is_partial_update:
                    self.console.print(
                        f"Validation error during partial update: {e}", style="red"
                    )
                    self.console.print(
                        "Hint: For partial updates, make sure the object exists and you're providing valid fields",
                        style="yellow",
                    )
                else:
                    self.console.print(f"Validation error: {e}", style="red")
            except APIError as e:
                error_message = str(e)
                self.console.print(f"API error: {error_message}", style="red")

                # Provide helpful feedback for common errors
                if (
                    "does not exist" in error_message.lower()
                    or "not found" in error_message.lower()
                ):
                    self.console.print(
                        "Hint: Make sure the object exists before attempting a partial update",
                        style="yellow",
                    )
                elif (
                    "permission" in error_message.lower()
                    or "access" in error_message.lower()
                ):
                    self.console.print(
                        "Hint: You may not have permission to modify this object",
                        style="yellow",
                    )
        except ValueError as e:
            self.console.print(f"Error: {e}", style="red")
            self.console.print(
                "Usage: set address-object <name> type <type> value <value> [description <text>] [tags <tag1,tag2,...>]"
            )

    def _display_object_as_table(self, address_obj: Any) -> None:
        """Display a single address object as a rich table.

        Args:
            address_obj: Address object (Pydantic model or dict)
        """
        # Create a table for display
        table = Table(
            title="Address Object Details", show_header=False, box=ROUNDED
        )
        table.add_column("Property", style="bold cyan", width=20)
        table.add_column("Value", style="green")

        # Add object properties to table
        name = (
            getattr(address_obj, "name", "")
            if hasattr(address_obj, "name")
            else address_obj.get("name", "")
        )
        table.add_row("Name", name)

        # Get and format type
        addr_type = _get_address_type(address_obj)
        table.add_row("Type", addr_type)

        # Get and format value
        value = _get_address_value(address_obj)
        table.add_row("Value", value)

        # Get description
        description = ""
        if hasattr(address_obj, "description"):
            description = getattr(address_obj, "description") or ""
        elif isinstance(address_obj, dict):
            description = address_obj.get("description", "")

        if description:
            table.add_row("Description", description)

        # Get tags
        tags = _get_address_tags(address_obj)
        if tags:
            table.add_row("Tags", tags)

        # Get folder
        folder = ""
        if hasattr(address_obj, "folder"):
            folder = getattr(address_obj, "folder")
        elif isinstance(address_obj, dict):
            folder = address_obj.get("folder", "")

        if folder:
            table.add_row("Folder", folder)

        # Get ID
        obj_id = ""
        if hasattr(address_obj, "id"):
            obj_id = getattr(address_obj, "id")
        elif isinstance(address_obj, dict):
            obj_id = address_obj.get("id", "")

        if obj_id:
            table.add_row("ID", str(obj_id))

        # Display the table
        self.console.print(table)

    def show_address_object(
        self,
        folder: str,
        name: Optional[str] = None,
        filter_criteria: Optional[Dict[str, str]] = None,
        limit: int = 50,
    ) -> None:
        """Show address object(s).

        Args:
            folder: Folder to show address object(s) from
            name: Name of specific address object to show (None for all)
            filter_criteria: Optional filter criteria for address objects
            limit: Maximum number of address objects to show
        """
        try:
            # Start timer for overall performance
            time.time()

            # Enable debug mode - shows timing information
            debug_timing = True

            # Create timing log function
            def log_timing(operation: str, duration: float) -> None:
                """Log timing information if debug_timing is enabled."""
                if debug_timing:
                    self.console.print(
                        f"[dim]DEBUG: {operation} took {duration:.3f} seconds[/dim]",
                        style="dim",
                    )

            if name is not None:
                # Show a specific address object
                api_start_time = time.time()

                # Show a loading message
                with self.console.status(
                    f"[bold yellow]Fetching address object '{name}'...[/bold yellow]"
                ):
                    address = self.api.get_object(folder, name)

                api_end_time = time.time()
                log_timing(
                    f"API call to get_object for '{name}'",
                    api_end_time - api_start_time,
                )

                # Check if the object was found
                if not address:
                    self.console.print(
                        f"Address object '{name}' not found in folder '{folder}'",
                        style="red",
                    )
                    return

                # Start timer for rendering
                render_start_time = time.time()

                # Display the object in a table
                self._display_object_as_table(address)

                render_end_time = time.time()
                log_timing(
                    "Rendering object details", render_end_time - render_start_time
                )
            else:
                # Show all address objects (or filtered ones)
                try:
                    api_start_time = time.time()

                    # Show a loading message
                    with self.console.status(
                        "[bold yellow]Fetching address objects...[/bold yellow]"
                    ):
                        addresses = self.api.list_objects(folder, filter_criteria)

                    api_end_time = time.time()
                    log_timing(
                        "API call to list_objects", api_end_time - api_start_time
                    )

                    if not addresses:
                        filter_text = ""
                        if filter_criteria:
                            filter_text = f" matching filter: {filter_criteria}"
                        self.console.print(
                            f"No address objects found in folder '{folder}'{filter_text}",
                            style="yellow",
                        )
                        return

                    # Start timer for rendering
                    render_start_time = time.time()

                    # Create a table for display
                    title = f"Address Objects in {folder}"
                    if filter_criteria:
                        filter_text = ", ".join(
                            [f"{k}='{v}'" for k, v in filter_criteria.items()]
                        )
                        title = (
                            f"Address Objects in {folder} (filtered by {filter_text})"
                        )

                    table = Table(title=title)
                    table.add_column("Name", style="cyan")
                    table.add_column("Type", style="green")
                    table.add_column("Value", style="blue")
                    table.add_column("Description", style="magenta")
                    table.add_column("Tags", style="yellow")

                    for addr in addresses[:limit]:
                        # Get name
                        name = (
                            getattr(addr, "name", "")
                            if hasattr(addr, "name")
                            else addr.get("name", "")
                        )

                        # Get address type
                        addr_type = _get_address_type(addr)

                        # Get address value
                        value = _get_address_value(addr)

                        # Get description
                        description = ""
                        if hasattr(addr, "description"):
                            description = getattr(addr, "description") or ""
                        elif isinstance(addr, dict):
                            description = addr.get("description", "")

                        # Get tags
                        tags = _get_address_tags(addr)

                        table.add_row(name, addr_type, value, description, tags)

                    self.console.print(table)

                    render_end_time = time.time()
                    log_timing("Rendering table", render_end_time - render_start_time)

                except ResourceNotFoundError as e:
                    self.console.print(f"Error: {e}", style="red")
                except APIError as e:
                    self.console.print(f"API error: {e}", style="red")
        except Exception as e:
            self.console.print(f"Error showing address object(s): {e}", style="red")

    def delete_address_object(self, folder: str, name: str) -> None:
        """Delete an address object.

        Args:
            folder: Folder containing the address object
            name: Name of the address object to delete
        """
        try:
            self.api.delete_object(folder, name)
            self.console.print(f"✅ - deleted address-object {name}", style="green")
        except ResourceNotFoundError as e:
            self.console.print(f"Error: {e}", style="red")
        except APIError as e:
            self.console.print(f"API error: {e}", style="red")