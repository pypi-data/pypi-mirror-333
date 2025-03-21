#!/usr/bin/env python3
"""SCM CLI main module."""

import argparse
import logging
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Set

import cmd2
from cmd2 import (
    Cmd2ArgumentParser,
    with_argparser,
    with_category,
)

# This line is no longer needed - logger is defined after imports

from rich.console import Console
from rich.table import Table
from rich.text import Text

# Import modules from the utils package with absolute imports
from scm.client import ScmClient
from scm.exceptions import AuthenticationError
from scm_cli.utils.config import load_oauth_credentials
from scm_cli.utils.db import CLIHistoryDB
from scm_cli.utils.help_formatter import help_registry, help_formatter
from scm_cli.utils.logging import set_log_level, get_log_levels
from scm_cli.utils.sdk_client import create_client, test_connection
from scm_cli.utils.state_manager import StateManager, CLIState, APICacheManager

# Import command modules
from .object.address_object.commands import AddressObjectCommands

# Set up logger
logger = logging.getLogger("scm_cli.cli.main")


@dataclass
class SCMState:
    """Class representing the current state of the SCM CLI.
    
    This extends the persistent CLIState with runtime-only state.
    """

    # Persistent state (loaded from storage)
    cli_state: CLIState
    
    # Services
    state_manager: StateManager
    api_cache: APICacheManager
    
    # Runtime-only state (not persisted)
    scm_client: Optional[ScmClient] = None
    history_db: CLIHistoryDB = field(default_factory=lambda: CLIHistoryDB())
    
    # Properties that delegate to cli_state
    @property
    def config_mode(self) -> bool:
        return self.cli_state.config_mode
    
    @config_mode.setter
    def config_mode(self, value: bool) -> None:
        self.cli_state.config_mode = value
        self.cli_state.save_state()
    
    @property
    def current_folder(self) -> Optional[str]:
        return self.cli_state.current_folder
    
    @current_folder.setter
    def current_folder(self, value: Optional[str]) -> None:
        if value:
            self.cli_state.set_folder(value)
        else:
            self.cli_state.exit_folder()
    
    @property
    def client_id(self) -> Optional[str]:
        return self.cli_state.client_id
    
    @client_id.setter
    def client_id(self, value: Optional[str]) -> None:
        if value:
            self.cli_state.set_user_info(value, self.username)
    
    @property
    def username(self) -> Optional[str]:
        return self.cli_state.username
    
    @username.setter
    def username(self, value: Optional[str]) -> None:
        if value and self.client_id:
            self.cli_state.set_user_info(self.client_id, value)
    
    @property
    def known_folders(self) -> Set[str]:
        return self.cli_state.known_folders
    
    @property
    def known_address_objects(self) -> Dict[str, Set[str]]:
        return self.cli_state.known_address_objects
        
    def add_known_address_object(self, folder: str, name: str) -> None:
        """Add an address object to known objects.
        
        Args:
            folder: Folder containing the object
            name: Object name
        """
        self.cli_state.add_known_address_object(folder, name)


# Command categories
CATEGORY_CONFIG = "Configuration Commands"
CATEGORY_ADDRESS = "Address Object Commands"
CATEGORY_GENERAL = "General Commands"
CATEGORY_HISTORY = "History Commands"
CATEGORY_SYSTEM = "System Commands"
CATEGORY_CACHE = "Cache Management Commands"


def _extract_username(client_id: str) -> str:
    """Extract username from client_id.

    Args:
        client_id: The full client_id which may contain email format

    Returns:
        Just the username part (before the @ symbol)
    """
    if not client_id:
        return "user"

    # Extract everything before the first @ symbol
    match = re.match(r"^([^@]+)@?.*$", client_id)
    if match:
        return match.group(1)

    return client_id


class SCMCLI(cmd2.Cmd):
    """SCM CLI command processor using cmd2."""

    def __init__(self) -> None:
        """Initialize the SCM CLI command processor."""
        # Initialize the cmd2 shell
        super().__init__(
            allow_cli_args=False,
            allow_redirection=False,
            terminators=[],
        )

        # Configure cmd2 settings
        self.self_in_help = False
        self.hidden_commands += [
            "alias",
            "macro",
            "run_pyscript",
            "run_script",
            "shell",
            "shortcuts",
            "py",
            "ipy",
        ]
        self.default_to_shell = False
        
        # Initialize help formatter with our console
        help_formatter.console = Console()  # Use the same console instance for consistent styling

        # Disable commands if they exist
        for cmd_name in [
            "alias",
            "macro",
            "run_pyscript",
            "run_script",
            "shell",
            "shortcuts",
        ]:
            if hasattr(self, f"do_{cmd_name}"):
                self.disable_command(cmd_name, "Command not available")

        # Initialize console first for setup messages
        self.console = Console()
        
        # Initialize state manager and persistent state
        self.console.print("Initializing state management...", style="dim")
        state_manager = StateManager()
        cli_state = CLIState.load_or_create(state_manager)
        api_cache = APICacheManager(state_manager)
        
        # Initialize state
        self.state = SCMState(
            cli_state=cli_state,
            state_manager=state_manager,
            api_cache=api_cache
        )
        
        # Clean up expired cache entries
        state_manager.clear_expired_cache()

        # Initialize SDK client
        self._initialize_sdk()

        # Set prompt
        self.update_prompt()

        # Configure cmd2 to use ? to display help
        self.continuation_prompt = "> "

        # Initialize command modules
        self._initialize_command_modules()

    def _initialize_command_modules(self) -> None:
        """Initialize the command modules."""
        # Initialize all command modules with the SCM client and cache manager
        self.address_object_commands = AddressObjectCommands(
            console=self.console, 
            client=self.state.scm_client,
            api_cache=self.state.api_cache  # Now using with proper serialization
        )

    # Use cmd2's built-in history mechanism but also store in our database
    def postcmd(self, stop: bool, statement: cmd2.Statement) -> bool:
        """Executed after the command is processed.

        Args:
            stop: True if the command loop should terminate
            statement: The command statement that was executed

        Returns:
            True if the command loop should terminate, False otherwise
        """
        # Skip recording certain commands
        skip_recording = ["history", "help", "exit", "quit"]
        should_record = statement.command and statement.command not in skip_recording

        # Record the command to the database
        if should_record:
            self.state.history_db.add_command(
                command=statement.raw.strip(),
                response="",  # We simplify by not capturing output for now
                folder=self.state.current_folder,
                success=True,
            )

        return super().postcmd(stop, statement)

    def precmd(self, statement: cmd2.Statement) -> cmd2.Statement:
        """Process the command before execution."""
        # Handle --help flag specially, ensuring it doesn't get processed as a command
        if "--help" in statement.raw:
            # Extract command parts from raw input by splitting and removing the flag
            parts = statement.raw.split()
            cmd_parts = [part for part in parts if part != "--help"]
            
            # Log what's being processed
            logger.debug(f"Help requested for: {cmd_parts}")
            
            # Process only first two parts if command has more than 2 parts to avoid recursion
            if len(cmd_parts) > 2:
                logger.debug(f"Limiting help to first two parts: {cmd_parts[:2]}")
                cmd_parts = cmd_parts[:2]
            
            # Process help request based on command parts
            if cmd_parts:
                help_displayed = self._show_help_for_command(cmd_parts)
            else:
                # No command specified, show main help
                self._show_main_help()
                help_displayed = True
                
            # If help was displayed, we're done
            if not help_displayed:
                logger.warning(f"Failed to display help for {cmd_parts}")
            
            # Return a completely empty statement
            # This prevents any further processing of the original command
            # Create with proper initialization instead of modifying after creation
            empty = cmd2.Statement("", command="", arg_list=[])
            return empty
            
        return statement

    def _initialize_sdk(self) -> None:
        """Initialize SCM client from OAuth credentials."""
        # Load credentials from .env file
        success, config = load_oauth_credentials()

        if not success:
            # Error messages already printed by load_oauth_credentials
            sys.exit(1)

        try:
            self.console.print("Initializing SCM client...", style="yellow")

            # Create SDK client
            self.state.scm_client = create_client(config)
            self.state.client_id = config.client_id

            # Extract username from client_id
            self.state.username = _extract_username(config.client_id)

            # Test connection
            try:
                test_connection(self.state.scm_client)
                # Show success message
                success_text = Text(
                    "✅ Client initialized successfully", style="bold green"
                )
                self.console.print(success_text)
                self.console.print()
                self.console.print("# " + "-" * 76)
                self.console.print("# Welcome to the SCM CLI for Strata Cloud Manager")
                self.console.print("# " + "-" * 76)
            except Exception as conn_error:
                self.console.print(
                    f"[bold red]Error:[/bold red] Failed to connect to SCM API: {str(conn_error)}",
                    style="red",
                )
                self.console.print(
                    "Please check your credentials in the .env file:", style="yellow"
                )
                self.console.print(
                    "  - Ensure SCM_CLIENT_ID is correct", style="yellow"
                )
                self.console.print(
                    "  - Ensure SCM_CLIENT_SECRET is correct", style="yellow"
                )
                self.console.print("  - Ensure SCM_TSG_ID is correct", style="yellow")
                self.console.print(
                    "  - Ensure you have valid API access to Strata Cloud Manager",
                    style="yellow",
                )
                sys.exit(1)
        except AuthenticationError as e:
            self.console.print(
                f"[bold red]Authentication Error:[/bold red] {e}", style="red"
            )
            self.console.print(
                "Please check your credentials in the .env file:", style="yellow"
            )
            self.console.print("  - Ensure SCM_CLIENT_ID is correct", style="yellow")
            self.console.print(
                "  - Ensure SCM_CLIENT_SECRET is correct", style="yellow"
            )
            self.console.print("  - Ensure SCM_TSG_ID is correct", style="yellow")
            sys.exit(1)
        except Exception as e:
            self.console.print(f"[bold red]Error:[/bold red] {e}", style="red")
            self.console.print("Stack trace:", style="dim")
            import traceback

            self.console.print(traceback.format_exc(), style="dim")
            sys.exit(1)

    def update_prompt(self) -> None:
        """Update the prompt based on the current state."""
        username = self.state.username or "user"

        if self.state.config_mode:
            if self.state.current_folder:
                self.prompt = f"{username}({self.state.current_folder})# "
            else:
                self.prompt = f"{username}@scm# "
        else:
            self.prompt = f"{username}@scm> "

    def emptyline(self) -> bool:
        """Do nothing on empty line."""
        return False

    def default(self, statement: cmd2.Statement) -> bool:
        """Handle unknown commands."""
        # Check if the command is empty (which can happen after help processing)
        if not statement.raw.strip():
            return False
            
        # Check if this is a help request that wasn't caught by precmd
        if "--help" in statement.raw:
            # Extract command parts from raw input by splitting and removing the flag
            parts = statement.raw.split()
            cmd_parts = [part for part in parts if part != "--help"]
            
            # Log what's being processed
            logger.debug(f"Help requested via default handler for: {cmd_parts}")
            
            # Process only first two parts if command has more than 2 parts to avoid recursion
            if len(cmd_parts) > 2:
                logger.debug(f"Limiting help to first two parts: {cmd_parts[:2]}")
                cmd_parts = cmd_parts[:2]
            
            # Process help request and skip further command processing
            help_displayed = self._show_help_for_command(cmd_parts)
            if not help_displayed:
                logger.warning(f"Failed to display help for {cmd_parts}")
            
            # Always return False to stop processing, even if help wasn't displayed
            return False
        
        # Normal unknown command processing
        self.console.print(f"Unknown command: {statement.raw}", style="red")
        self.console.print("Type 'help' for a list of commands or append '--help' to any command for specific help.", style="yellow")
        return False

    def _show_help_for_command(self, cmd_parts: List[str]) -> bool:
        """Show help for a command using Rich tables.
        
        Args:
            cmd_parts: Command parts (e.g., ["set", "address-object"])
            
        Returns:
            True if help was displayed, False otherwise
        """
        # Log the command parts for debugging
        logger.debug(f"Showing help for command parts: {cmd_parts}")
        
        if not cmd_parts:
            # Show general help
            commands = help_registry.get_available_commands()
            if commands:
                help_formatter.print_help_table(
                    data=commands,
                    title="Available Commands",
                    table_type="command"
                )
            else:
                self.console.print("No commands registered for help. Using default help.")
                # Don't call do_help here to avoid recursion
                self._show_main_help()
            return True
            
        # Handle command with potential subcommand
        cmd = cmd_parts[0]
        logger.debug(f"Looking for primary command: {cmd}")
        
        # Direct lookup for command help from registry first
        if len(cmd_parts) == 1:
            # Command-level help
            help_data = help_registry.get_command_help(cmd)
            logger.debug(f"Help data for {cmd}: {'Found' if help_data else 'Not found'}")
            
            if help_data:
                # We have help for this command in registry
                help_formatter.print_command_help(
                    command_name=cmd,
                    description=help_data["description"],
                    required_args=help_data["required_args"],
                    optional_args=help_data["optional_args"],
                    examples=help_data["examples"],
                    notes=help_data["notes"]
                )
                
                # Show available subcommands if any
                subcommands = help_registry.get_available_subcommands(cmd)
                if subcommands:
                    help_formatter.print_help_table(
                        data=subcommands,
                        title=f"Available {cmd.title()} Subcommands",
                        table_type="command"
                    )
                return True
            else:
                # Look for built-in command
                cmd_method = getattr(self, f"do_{cmd}", None)
                if cmd_method and cmd_method.__doc__:
                    # Use a simple docstring display instead of calling do_help
                    from rich.panel import Panel
                    from rich.box import ROUNDED
                    
                    self.console.print(
                        Panel(
                            cmd_method.__doc__.strip(), 
                            title=f"Help: {cmd}",
                            border_style="cyan", 
                            box=ROUNDED
                        )
                    )
                    return True
                else:
                    self.console.print(f"No help available for command: {cmd}", style="yellow")
                    return False
        
        elif len(cmd_parts) >= 2:
            # Subcommand help
            subcmd = cmd_parts[1]
            logger.debug(f"Looking for subcommand help: {cmd} {subcmd}")
            
            # Try to get combined help first (for cases like "address-object")
            if cmd in ["set", "show", "delete"]:
                # These commands commonly use object types like "address-object"
                help_data = help_registry.get_subcommand_help(cmd, subcmd)
                logger.debug(f"Help data for {cmd} {subcmd}: {'Found' if help_data else 'Not found'}")
                
                if help_data:
                    # We have help for this subcommand in registry
                    help_formatter.print_command_help(
                        command_name=f"{cmd} {subcmd}",
                        description=help_data["description"],
                        required_args=help_data["required_args"],
                        optional_args=help_data["optional_args"],
                        examples=help_data["examples"],
                        notes=help_data["notes"]
                    )
                    return True
            
            # If we reach here, no subcommand help was found
            # Try showing help for the primary command
            help_data = help_registry.get_command_help(cmd)
            if help_data:
                help_formatter.print_command_help(
                    command_name=cmd,
                    description=help_data["description"],
                    required_args=help_data["required_args"],
                    optional_args=help_data["optional_args"],
                    examples=help_data["examples"],
                    notes=help_data["notes"]
                )
                
                # Show available subcommands
                subcommands = help_registry.get_available_subcommands(cmd)
                if subcommands:
                    help_formatter.print_help_table(
                        data=subcommands,
                        title=f"Available {cmd.title()} Subcommands",
                        table_type="command"
                    )
                return True
            else:
                # No subcommand help found, but we can still be helpful
                self.console.print(f"No help available for: {' '.join(cmd_parts)}", style="yellow")
                return False
                
        # Log that the user used the help system
        logger.debug(f"User requested help for: {' '.join(cmd_parts)}")
        return True

    # Tab completion helpers for folder names, object names, etc.
    # ... (implement as needed)

    # Core commands
    def do_help(self, statement_or_string):
        """Show help for a command."""
        # Track call depth to prevent infinite recursion
        if not hasattr(self, '_help_call_depth'):
            self._help_call_depth = 0
        self._help_call_depth += 1
        
        # Guard against excessive recursion
        if self._help_call_depth > 2:
            self.console.print("Help recursion detected, stopping help display", style="red")
            self._help_call_depth = 0
            return
            
        try:
            # Empty help command - display our main Rich-formatted help directly
            if not statement_or_string or (isinstance(statement_or_string, str) and not statement_or_string.strip()):
                self._show_main_help()
                return
                
            # Specific command help - try our fancy help system first
            if isinstance(statement_or_string, str) and statement_or_string.strip():
                cmd_parts = statement_or_string.strip().split()
                # Try our fancy help system first - note this now always returns True
                help_displayed = self._show_help_for_command(cmd_parts)
                if help_displayed:
                    return
            
            # Fall back to cmd2's help for specific commands we don't know about
            import io
            from contextlib import redirect_stdout
            
            # Capture cmd2's help output
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                super().do_help(statement_or_string)
            
            # Get the captured output
            help_text = buffer.getvalue()
            
            # Format specific command help in a Rich panel
            cmd_name = statement_or_string.strip() if isinstance(statement_or_string, str) else "help"
            
            # Import Rich components
            from rich.panel import Panel
            from rich.box import ROUNDED
            
            # Display the help text in a panel
            self.console.print(Panel(help_text, title=f"Help: {cmd_name}", border_style="cyan", box=ROUNDED))
        finally:
            # Always decrement the call depth when exiting
            self._help_call_depth -= 1
        
    def _show_main_help(self):
        """Show main help with all commands in Rich formatted tables."""
        # Import Rich components
        from rich.table import Table
        from rich.box import ROUNDED
        
        # Get all visible commands
        visible_commands = self.get_visible_commands()
        
        # Group commands by category
        commands_by_category = {}
        
        # Try to map commands to our predefined categories
        # These categories should match the ones defined as constants in this class
        categories = [
            CATEGORY_CONFIG, CATEGORY_ADDRESS, CATEGORY_GENERAL, 
            CATEGORY_HISTORY, CATEGORY_SYSTEM, CATEGORY_CACHE
        ]
        
        # Initialize category lists
        for category in categories:
            commands_by_category[category] = []
        
        # Add an "Uncategorized" category
        commands_by_category["Uncategorized"] = []
        
        # Group commands by their categories
        for cmd_name in visible_commands:
            cmd_func = getattr(self, f"do_{cmd_name}")
            category = None
            
            # Try to determine the category from the function attribute
            for cat in categories:
                # Check if this command belongs to this category
                if hasattr(cmd_func, "category") and cmd_func.category == cat:
                    category = cat
                    break
                
            # If we couldn't find a category, use function name as a hint
            if not category:
                if cmd_name in ["set", "show", "delete"]:
                    category = CATEGORY_ADDRESS
                elif cmd_name in ["configure", "edit"]:
                    category = CATEGORY_CONFIG
                elif cmd_name in ["exit", "quit"]:
                    category = CATEGORY_GENERAL
                elif cmd_name in ["history"]:
                    category = CATEGORY_HISTORY
                elif cmd_name in ["logger"]:
                    category = CATEGORY_SYSTEM
                elif cmd_name in ["cache"]:
                    category = CATEGORY_CACHE
                else:
                    category = "Uncategorized"
            
            # Get the command description from the docstring
            docstring = cmd_func.__doc__ or ""
            description = docstring.strip().split('\n')[0] if docstring else ""
            
            # Add to the appropriate category
            commands_by_category[category].append((cmd_name, description))
        
        # Now display each category in a Rich table
        for category, commands in commands_by_category.items():
            # Skip empty categories
            if not commands:
                continue
                
            # Create a Rich table for this category
            table = Table(title=category, box=ROUNDED, title_style="bold cyan")
            table.add_column("Command", style="cyan")
            table.add_column("Description", style="green")
            
            # Add commands to the table
            for cmd_name, description in sorted(commands):
                table.add_row(cmd_name, description)
                
            # Display the table
            self.console.print(table)
            
        # Add helpful hint at the bottom
        self.console.print("\n[italic]Use 'help <command>' or '<command> --help' for more information about a specific command.[/italic]")
    
    def _show_formatted_categories(self, help_text: str):
        """Format the command list by category using Rich tables."""
        # Debug output to see what we're parsing
        logger.debug(f"Parsing help text: {help_text[:100]}...")
        
        # Parse the help text to extract categories and commands
        lines = help_text.split('\n')
        categories = {}
        current_category = None
        i = 0
        
        # Skip introductory text
        while i < len(lines) and not lines[i].startswith('='):
            i += 1
            
        # Process the lines
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip blank lines
            if not line:
                i += 1
                continue
                
            # If this is a line of equal signs, it's a category header underline
            if line.startswith('=') and i > 0 and lines[i-1].strip():
                # The category name is the line before the underline
                current_category = lines[i-1].strip()
                categories[current_category] = []
                i += 1
                continue
                
            # If we have a current category and this isn't a blank line or another header
            if current_category and '  ' in line:
                # This line contains a command and its description
                parts = line.split('  ', 1)
                if len(parts) == 2:
                    cmd_name = parts[0].strip()
                    description = parts[1].strip()
                    categories[current_category].append((cmd_name, description))
            
            i += 1
            
        # Debug the parsed categories
        logger.debug(f"Parsed categories: {list(categories.keys())}")
        
        # Import Rich components just once
        from rich.table import Table
        from rich.box import ROUNDED
        
        # Now display each category
        for category, commands in categories.items():
            if not commands:
                continue
                
            # Create Rich table with rounded borders
            table = Table(title=category, box=ROUNDED, title_style="bold cyan")
            table.add_column("Command", style="cyan")
            table.add_column("Description", style="green")
            
            # Add commands to table
            for cmd_name, description in sorted(commands):
                table.add_row(cmd_name, description)
                
            # Display the table
            self.console.print(table)
            
        # If we didn't find any categories, display a basic help message
        if not categories:
            self.console.print("\n[bold cyan]Available Commands[/bold cyan]\n")
            self.console.print(help_text)
            self.console.print("\n[italic]Use 'help <command>' for more information about a specific command.[/italic]")
        
    # Method removed - replaced by improved _show_help_for_command method
    
    @with_category(CATEGORY_GENERAL)
    def do_exit(self, _: cmd2.Statement) -> bool:
        """Exit the current mode or the CLI."""
        if self.state.current_folder:
            self.state.current_folder = None
            self.update_prompt()
            return False
        elif self.state.config_mode:
            self.state.config_mode = False
            self.update_prompt()
            return False
        else:
            return True

    @with_category(CATEGORY_GENERAL)
    def do_quit(self, _: cmd2.Statement) -> bool:
        """Exit the CLI."""
        return True

    # History command
    history_parser = Cmd2ArgumentParser(description="Show command history")
    history_parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of history entries to show per page",
    )
    history_parser.add_argument(
        "--page", type=int, default=1, help="Page number to display (starting from 1)"
    )
    history_parser.add_argument("--folder", help="Filter history by folder")
    history_parser.add_argument("--filter", help="Filter history by command content")
    history_parser.add_argument(
        "--clear", action="store_true", help="Clear command history"
    )
    history_parser.add_argument(
        "--id", type=int, help="Show details of a specific history entry"
    )

    @with_category(CATEGORY_HISTORY)
    @with_argparser(history_parser)
    def do_history(self, args: argparse.Namespace) -> None:
        """Show command history."""
        if args.clear:
            self.state.history_db.clear_history()
            self.console.print("Command history cleared", style="green")
            return

        # If an ID is specified, show details for that specific entry
        if args.id is not None:
            entry = self.state.history_db.get_history_entry(args.id)
            if not entry:
                self.console.print(
                    f"History entry with ID {args.id} not found", style="red"
                )
                return

            object_id, timestamp, command, response, folder, success = entry

            # Format the timestamp
            try:
                dt = datetime.fromisoformat(timestamp)
                formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                formatted_time = timestamp

            # Display the history entry details
            self.console.print(f"[bold cyan]History Entry #{object_id}[/bold cyan]")
            self.console.print(f"[bold]Timestamp:[/bold] {formatted_time}")
            self.console.print(f"[bold]Folder:[/bold] {folder or 'None'}")
            self.console.print(f"[bold]Command:[/bold] {command}")
            self.console.print("\n[bold]Response:[/bold]")
            self.console.print(response)
            return

        # Validate page number
        if args.page < 1:
            self.console.print("Page number must be 1 or greater", style="red")
            return

        # Get history from database with pagination
        history_items, total_count = self.state.history_db.get_history(
            limit=args.limit,
            page=args.page,
            folder=args.folder,
            command_filter=args.filter,
        )

        if not history_items:
            self.console.print("No command history found", style="yellow")
            return

        # Calculate pagination info
        total_pages = (total_count + args.limit - 1) // args.limit  # Ceiling division

        # Create table for display
        title = f"Command History (Page {args.page} of {total_pages})"
        if args.folder or args.filter:
            filters = []
            if args.folder:
                filters.append(f"folder='{args.folder}'")
            if args.filter:
                filters.append(f"filter='{args.filter}'")
            title += f" [Filtered by: {', '.join(filters)}]"

        table = Table(title=title)
        table.add_column("ID", style="cyan", justify="right")
        table.add_column("Timestamp", style="magenta")
        table.add_column("Folder", style="green")
        table.add_column("Command", style="blue")

        # Add history items to table
        for object_id, timestamp, command, response, folder, success in history_items:
            # Format the timestamp
            try:
                dt = datetime.fromisoformat(timestamp)
                formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                formatted_time = timestamp

            table.add_row(str(object_id), formatted_time, folder or "", command)

        self.console.print(table)

        # Show pagination help
        pagination_help = []
        if args.page > 1:
            pagination_help.append(f"'history --page {args.page-1}' for previous page")
        if args.page < total_pages:
            pagination_help.append(f"'history --page {args.page+1}' for next page")

        if pagination_help:
            self.console.print(
                f"\nPagination: {' | '.join(pagination_help)}", style="dim"
            )

        self.console.print(
            "\nTip: Use 'history --id <name>' to view the full details of a specific entry",
            style="dim",
        )

    @with_category(CATEGORY_CONFIG)
    def do_configure(self, _: cmd2.Statement) -> bool:
        """Enter configuration mode."""
        if not self.state.config_mode:
            self.state.config_mode = True
            self.update_prompt()
        return False

    # Edit command
    edit_parser = Cmd2ArgumentParser(description="Edit a specific folder")
    edit_parser.add_argument(
        "object_type", choices=["folder"], help="Object type to edit"
    )
    edit_parser.add_argument("name", help="Name of the folder to edit")

    @with_category(CATEGORY_CONFIG)
    @with_argparser(edit_parser)
    def do_edit(self, args: argparse.Namespace) -> None:
        """Edit a specific folder."""
        if not self.state.config_mode:
            self.console.print(
                "Command only available in configuration mode", style="red"
            )
            return

        folder = args.name
        self.state.current_folder = folder

        # Add folder to known folders for autocompletion
        self.state.known_folders.add(folder)

        self.update_prompt()

    @with_category(CATEGORY_ADDRESS)
    def do_set(self, statement: cmd2.Statement) -> None:
        """Set an object's properties."""
        # Parse command
        args = statement.arg_list

        if not args:
            self.console.print("Missing object type", style="red")
            self.console.print(
                "Usage: set address-object <name> type <type> value <value> [description <text>] [tags <tag1,tag2,...>]"
            )
            return

        object_type = args[0]

        if not self.state.config_mode or not self.state.current_folder:
            self.console.print(
                "Command only available in folder edit mode", style="red"
            )
            return

        if not self.state.scm_client:
            self.console.print("No SCM client available.", style="red")
            return

        # Delegate to appropriate command handler
        if object_type == "address-object":
            self.address_object_commands.set_address_object(
                self.state.current_folder, args
            )
        else:
            self.console.print(f"Unknown object type: {object_type}", style="red")

    # Delete command
    delete_parser = Cmd2ArgumentParser(description="Delete an object")
    delete_subparsers = delete_parser.add_subparsers(
        title="objects", dest="object_type"
    )

    # Address object subparser
    addr_del_parser = delete_subparsers.add_parser(
        "address-object", help="Delete an address object"
    )
    addr_del_parser.add_argument("name", help="Name of the address object")

    # Logger command
    logger_parser = Cmd2ArgumentParser(description="Control logging levels")
    logger_subparsers = logger_parser.add_subparsers(
        title="logger-commands", dest="subcommand"
    )
    
    # Show logger levels
    logger_show_parser = logger_subparsers.add_parser(
        "show", help="Show current log levels"
    )
    
    # Set logger level
    logger_set_parser = logger_subparsers.add_parser(
        "set", help="Set log level for a module"
    )
    logger_set_parser.add_argument(
        "level", 
        choices=["debug", "info", "warning", "error", "critical"],
        help="Log level to set"
    )
    logger_set_parser.add_argument(
        "--module", 
        help="Optional module name (default: scm_cli for root logger)"
    )
    
    # Cache command
    cache_parser = Cmd2ArgumentParser(description="Manage API response cache")
    cache_subparsers = cache_parser.add_subparsers(
        title="cache-commands", dest="subcommand"
    )
    
    # Show cache stats
    cache_show_parser = cache_subparsers.add_parser(
        "stats", help="Show cache statistics"
    )
    
    # Clear cache
    cache_clear_parser = cache_subparsers.add_parser(
        "clear", help="Clear the API response cache"
    )
    cache_clear_parser.add_argument(
        "--endpoint",
        help="Optional endpoint to clear (e.g., 'address/list')"
    )

    @with_category(CATEGORY_ADDRESS)
    @with_argparser(delete_parser)
    def do_delete(self, args: argparse.Namespace) -> None:
        """Delete an object."""
        if not self.state.config_mode or not self.state.current_folder:
            self.console.print(
                "Command only available in folder edit mode", style="red"
            )
            return

        if not self.state.scm_client:
            self.console.print("No SCM client available.", style="red")
            return

        # Delegate to appropriate command handler
        if args.object_type == "address-object":
            self.address_object_commands.delete_address_object(
                self.state.current_folder, args.name
            )
        else:
            self.console.print(f"Unknown object type: {args.object_type}", style="red")

    # Show command
    show_parser = Cmd2ArgumentParser(description="Show object details")
    show_subparsers = show_parser.add_subparsers(title="objects", dest="object_type")

    # Address object subparser
    addr_show_parser = show_subparsers.add_parser(
        "address-object", help="Show address object details"
    )
    addr_show_parser.add_argument(
        "name",
        nargs="?",
        default=None,
        help="Name of the address object to show (optional - if omitted, shows all objects)",
    )

    # Address objects filter subparser
    addr_filter_parser = show_subparsers.add_parser(
        "address-objects-filter", help="Search and filter address objects"
    )
    addr_filter_parser.add_argument("--name", help="Filter by name (substring match)")
    addr_filter_parser.add_argument(
        "--type",
        help="Filter by type (exact match)",
        choices=["ip-netmask", "ip-range", "fqdn"],
    )
    addr_filter_parser.add_argument("--value", help="Filter by value (substring match)")
    addr_filter_parser.add_argument("--tag", help="Filter by tag (substring match)")

    @with_category(CATEGORY_ADDRESS)
    @with_argparser(show_parser)
    def do_show(self, args: argparse.Namespace) -> None:
        """Show object details."""
        if not self.state.config_mode:
            self.console.print(
                "Command only available in configuration mode", style="red"
            )
            return

        if not self.state.scm_client:
            self.console.print("No SCM client available.", style="red")
            return

        folder = self.state.current_folder
        if not folder:
            self.console.print("No folder selected", style="red")
            return

        # Map CLI types to SDK types for filtering
        cli_to_sdk_type = {"ip-netmask": "ip", "ip-range": "range", "fqdn": "fqdn"}

        # Delegate to appropriate command handler
        if args.object_type == "address-object":
            self.address_object_commands.show_address_object(folder, args.name)
        elif args.object_type == "address-objects-filter":
            # Build filter criteria from arguments
            filter_criteria = {}

            if args.name:
                filter_criteria["name"] = args.name

            if args.type:
                filter_criteria["type"] = cli_to_sdk_type.get(args.type, args.type)

            if args.value:
                filter_criteria["value"] = args.value

            if args.tag:
                filter_criteria["tag"] = args.tag

            self.address_object_commands.show_address_object(
                folder, None, filter_criteria=filter_criteria
            )
        else:
            self.console.print(f"Unknown object type: {args.object_type}", style="red")
    
    @with_category(CATEGORY_SYSTEM)
    @with_argparser(logger_parser)
    def do_logger(self, args: argparse.Namespace) -> None:
        """Control logging levels."""
        if args.subcommand == "show":
            # Get the current log levels
            log_levels = get_log_levels()
            
            # Create a table for display
            table = Table(title="Logging Levels")
            table.add_column("Logger", style="cyan")
            table.add_column("Level", style="green")
            
            # Add each logger to the table
            for log in log_levels:
                table.add_row(log["name"], log["level"].upper())
            
            self.console.print(table)
            
        elif args.subcommand == "set":
            # Set the log level
            module = args.module or "scm_cli"
            if set_log_level(args.level, module):
                self.console.print(
                    f"✅ Log level for '{module}' set to {args.level.upper()}", 
                    style="green"
                )
            else:
                self.console.print(
                    f"❌ Failed to set log level for '{module}'", 
                    style="red"
                )
    
    @with_category(CATEGORY_CACHE)
    @with_argparser(cache_parser)
    def do_cache(self, args: argparse.Namespace) -> None:
        """Manage API response cache."""
        if args.subcommand == "stats":
            # Get cache statistics
            stats = self.state.api_cache.get_cache_stats()
            
            # Display overall stats
            self.console.print(f"Total cached API responses: {stats['total_count']}", style="cyan")
            
            if stats['total_count'] > 0:
                # Create table of endpoints
                table = Table(title="Cache by Endpoint")
                table.add_column("Endpoint", style="green")
                table.add_column("Entries", style="cyan", justify="right")
                
                for endpoint, count in stats['endpoint_counts'].items():
                    table.add_row(endpoint, str(count))
                
                self.console.print(table)
                
                # Add expiration note
                self.console.print(
                    "Note: Cache entries automatically expire based on their TTL settings.", 
                    style="dim"
                )
                
        elif args.subcommand == "clear":
            if args.endpoint:
                # Clear specific endpoint cache
                count = self.state.api_cache.invalidate_by_prefix(f"api:{args.endpoint}")
                self.console.print(
                    f"✅ Cleared {count} cache entries for endpoint '{args.endpoint}'", 
                    style="green"
                )
            else:
                # Clear all cache
                count = self.state.api_cache.clear_all_cache()
                self.console.print(
                    f"✅ Cleared all API cache ({count} entries)", 
                    style="green"
                )


def main() -> None:
    """Run the SCM CLI."""
    console = Console()
    console.print("Entering SCM CLI", style="bold green")
    try:
        cli = SCMCLI()
        cli.cmdloop()
    except KeyboardInterrupt:
        console.print("\nExiting SCM CLI", style="bold yellow")
    print("$")


if __name__ == "__main__":
    main()