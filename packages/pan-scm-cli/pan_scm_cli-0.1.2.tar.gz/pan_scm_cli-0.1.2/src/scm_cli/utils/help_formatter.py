"""Help formatter for SCM CLI using Rich tables."""

import importlib
import logging
from typing import List, Dict, Any, Optional, Tuple

from rich.box import ROUNDED
from rich.console import Console
from rich.table import Table

# Set up logger
logger = logging.getLogger("scm_cli.utils.help_formatter")


class HelpFormatter:
    """Format help content using Rich tables for consistent and attractive display."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize the help formatter.
        
        Args:
            console: Optional Console for rich text output
        """
        self.console = console or Console()
        
        # Color schemes for different table types
        self.color_schemes = {
            "command": {
                "headers": ["Command", "Description"], 
                "styles": ["cyan", "green"],
                "title_style": "bold cyan"
            },
            "argument": {
                "headers": ["Argument", "Description"], 
                "styles": ["yellow", "blue"],
                "title_style": "bold yellow"
            },
            "option": {
                "headers": ["Option", "Description"], 
                "styles": ["cyan", "green"],
                "title_style": "bold cyan"
            },
            "example": {
                "headers": ["Example", "Description"], 
                "styles": ["magenta", "blue"],
                "title_style": "bold magenta"
            },
        }
    
    def _create_rich_table(self, 
                          data: List[Tuple[str, str]], 
                          title: str, 
                          table_type: str = "command",
                          widths: Optional[List[int]] = None) -> Table | None:
        """Create a styled Rich table.
        
        Args:
            data: List of tuples with (column1, column2) values
            title: Table title
            table_type: Type of table (command, argument, option, example)
            widths: Optional column widths
            
        Returns:
            Rich Table object
        """
        if not data:
            return None
            
        # Get scheme for this table type
        scheme = self.color_schemes.get(table_type, self.color_schemes["command"])
        headers = scheme["headers"]
        styles = scheme["styles"]
        title_style = scheme["title_style"]
        
        # Create Rich table with rounded borders
        table = Table(title=title, box=ROUNDED, title_style=title_style)
        
        # Add columns with appropriate styles
        for i, header in enumerate(headers):
            width = None if not widths or i >= len(widths) else widths[i]
            table.add_column(header, style=styles[i], width=width)
        
        # Add rows
        for row in data:
            table.add_row(*row)
            
        return table
    
    def print_help_table(self, 
                        data: List[Tuple[str, str]], 
                        title: str, 
                        table_type: str = "command") -> None:
        """Print a styled help table to the console.
        
        Args:
            data: List of tuples with (column1, column2) values
            title: Table title
            table_type: Type of table (command, argument, option, example)
        """
        if not data:
            return
            
        table = self._create_rich_table(data, title, table_type)
        if table:
            self.console.print(table)
    
    def print_command_help(self, 
                          command_name: str, 
                          description: str, 
                          required_args: List[Tuple[str, str]] = None, 
                          optional_args: List[Tuple[str, str]] = None,
                          examples: List[Tuple[str, str]] = None,
                          notes: List[str] = None) -> None:
        """Print comprehensive help for a command to the console.
        
        Args:
            command_name: Name of the command
            description: Description of the command
            required_args: List of (name, description) tuples for required arguments
            optional_args: List of (name, description) tuples for optional arguments
            examples: List of (example, description) tuples
            notes: List of additional notes
        """
        # Print command header and description
        self.console.print(f"\n[bold]## {command_name} ##[/bold]\n")
        self.console.print(f"{description}\n")
        
        # Required arguments table
        if required_args:
            req_table = self._create_rich_table(
                required_args, "Required Arguments", "argument"
            )
            self.console.print(req_table)
        
        # Optional arguments table
        if optional_args:
            opt_table = self._create_rich_table(
                optional_args, "Optional Arguments", "option"
            )
            self.console.print(opt_table)
        
        # Examples table
        if examples:
            ex_table = self._create_rich_table(
                examples, "Examples", "example"
            )
            self.console.print(ex_table)
            
        # Notes section
        if notes:
            self.console.print("\n[bold]Notes:[/bold]")
            for i, note in enumerate(notes, 1):
                self.console.print(f"{i}. {note}")
            self.console.print("")


# Help content registry - stores help content for different commands and objects
class HelpRegistry:
    """Registry for managing help content across the application."""
    
    def __init__(self):
        """Initialize the help registry."""
        self._command_help = {}
        self._subcommand_help = {}
        self._module_help_providers = {}
    
    def register_command_help(self, 
                             command: str,
                             description: str,
                             required_args: List[Tuple[str, str]] = None,
                             optional_args: List[Tuple[str, str]] = None,
                             examples: List[Tuple[str, str]] = None,
                             notes: List[str] = None) -> None:
        """Register help content for a command.
        
        Args:
            command: Command name
            description: Command description
            required_args: Required arguments
            optional_args: Optional arguments
            examples: Usage examples
            notes: Additional notes
        """
        self._command_help[command] = {
            "description": description,
            "required_args": required_args or [],
            "optional_args": optional_args or [],
            "examples": examples or [],
            "notes": notes or []
        }
    
    def register_subcommand_help(self,
                               command: str,
                               subcommand: str,
                               description: str,
                               required_args: List[Tuple[str, str]] = None,
                               optional_args: List[Tuple[str, str]] = None,
                               examples: List[Tuple[str, str]] = None,
                               notes: List[str] = None) -> None:
        """Register help content for a subcommand.
        
        Args:
            command: Parent command name
            subcommand: Subcommand name
            description: Subcommand description
            required_args: Required arguments
            optional_args: Optional arguments
            examples: Usage examples
            notes: Additional notes
        """
        key = f"{command} {subcommand}"
        self._subcommand_help[key] = {
            "description": description,
            "required_args": required_args or [],
            "optional_args": optional_args or [],
            "examples": examples or [],
            "notes": notes or []
        }
    
    def register_module_help_provider(self, module_path: str, help_class_name: str) -> None:
        """Register a module that provides help content.
        
        Args:
            module_path: Import path to the module (e.g., "scm_cli.cli.object.address_object.help")
            help_class_name: Name of the help class within the module
        """
        self._module_help_providers[module_path] = help_class_name
    
    def get_command_help(self, command: str) -> Optional[Dict[str, Any]]:
        """Get help content for a command.
        
        Args:
            command: Command name
            
        Returns:
            Help content dictionary or None if not found
        """
        logger.debug(f"Looking for help for command: {command}")
        
        # Try to get from directly registered commands first
        help_data = self._command_help.get(command)
        if help_data:
            logger.debug(f"Found help for {command} in direct registry")
            return help_data
            
        # Try to find from registered modules
        for module_path, class_name in self._module_help_providers.items():
            logger.debug(f"Searching for {command} help in module: {module_path}.{class_name}")
            try:
                module = importlib.import_module(module_path)
                help_class = getattr(module, class_name, None)
                if help_class and hasattr(help_class, "get_command_help"):
                    help_data = help_class.get_command_help(command)
                    if help_data:
                        logger.debug(f"Found help for {command} in module {module_path}")
                        return help_data
                    else:
                        logger.debug(f"Module {module_path} returned no help for {command}")
            except (ImportError, AttributeError) as e:
                logger.warning(f"Error loading help from {module_path}: {e}")
                
        logger.debug(f"No help found for command: {command}")
        return None
    
    def get_subcommand_help(self, command: str, subcommand: str) -> Optional[Dict[str, Any]]:
        """Get help content for a subcommand.
        
        Args:
            command: Parent command name
            subcommand: Subcommand name
            
        Returns:
            Help content dictionary or None if not found
        """
        logger.debug(f"Looking for help for subcommand: {command} {subcommand}")
        
        # Try to get from directly registered subcommands first
        key = f"{command} {subcommand}"
        help_data = self._subcommand_help.get(key)
        if help_data:
            logger.debug(f"Found help for {key} in direct registry")
            return help_data
            
        # Try to find from registered modules
        for module_path, class_name in self._module_help_providers.items():
            logger.debug(f"Searching for {key} help in module: {module_path}.{class_name}")
            try:
                module = importlib.import_module(module_path)
                help_class = getattr(module, class_name, None)
                if help_class and hasattr(help_class, "get_subcommand_help"):
                    help_data = help_class.get_subcommand_help(command, subcommand)
                    if help_data:
                        logger.debug(f"Found help for {key} in module {module_path}")
                        return help_data
                    else:
                        logger.debug(f"Module {module_path} returned no help for {key}")
            except (ImportError, AttributeError) as e:
                logger.warning(f"Error loading subcommand help from {module_path}: {e}")
                
        logger.debug(f"No help found for subcommand: {key}")
        return None
    
    def get_available_commands(self) -> List[Tuple[str, str]]:
        """Get list of available commands with descriptions.
        
        Returns:
            List of (command, description) tuples
        """
        # Start with directly registered commands
        result = [(cmd, data["description"]) 
                for cmd, data in self._command_help.items()]
                
        # Add commands from registered modules
        for module_path, class_name in self._module_help_providers.items():
            try:
                module = importlib.import_module(module_path)
                help_class = getattr(module, class_name, None)
                if help_class and hasattr(help_class, "get_available_commands"):
                    module_commands = help_class.get_available_commands()
                    if module_commands:
                        result.extend(module_commands)
            except (ImportError, AttributeError) as e:
                logger.warning(f"Error loading available commands from {module_path}: {e}")
                
        return result
    
    def get_available_subcommands(self, command: str) -> List[Tuple[str, str]]:
        """Get list of available subcommands for a command.
        
        Args:
            command: Parent command name
            
        Returns:
            List of (subcommand, description) tuples
        """
        # Start with directly registered subcommands
        result = []
        for key, data in self._subcommand_help.items():
            if key.startswith(f"{command} "):
                subcommand = key[len(command)+1:]
                result.append((subcommand, data["description"]))
                
        # Add subcommands from registered modules
        for module_path, class_name in self._module_help_providers.items():
            try:
                module = importlib.import_module(module_path)
                help_class = getattr(module, class_name, None)
                if help_class and hasattr(help_class, "get_available_subcommands"):
                    module_subcommands = help_class.get_available_subcommands(command)
                    if module_subcommands:
                        result.extend(module_subcommands)
            except (ImportError, AttributeError) as e:
                logger.warning(f"Error loading available subcommands from {module_path}: {e}")
                
        return result


# Initialize global registry and formatter instances
help_registry = HelpRegistry()
help_formatter = HelpFormatter()


# Register core commands (these are kept in the central registry for simplicity)
def register_core_help_content():
    """Register help content for core commands that aren't module-specific."""
    
    # Configure command
    help_registry.register_command_help(
        command="configure",
        description="Enter configuration mode",
        examples=[
            ("configure", "Enter configuration mode")
        ],
        notes=[
            "Configuration mode allows you to make changes to objects.",
            "Use exit to return to operational mode."
        ]
    )
    
    # Edit folder subcommand
    help_registry.register_subcommand_help(
        command="edit",
        subcommand="folder",
        description="Edit a specific folder",
        required_args=[
            ("<folder-name>", "Name of the folder to edit")
        ],
        examples=[
            ("edit folder Texas", "Edit the 'Texas' folder")
        ],
        notes=[
            "You must be in configuration mode to use this command.",
            "Use exit to return to the previous mode."
        ]
    )
    
    # Exit command
    help_registry.register_command_help(
        command="exit",
        description="Exit the current mode or the CLI",
        examples=[
            ("exit", "Exit configuration mode or the current folder")
        ],
        notes=[
            "If in a folder context, exit returns to configuration mode.",
            "If in configuration mode, exit returns to operational mode.",
            "If in operational mode, exit terminates the CLI."
        ]
    )
    
    # Quit command
    help_registry.register_command_help(
        command="quit",
        description="Exit the CLI",
        examples=[
            ("quit", "Exit the CLI completely")
        ]
    )


# Register module-specific help providers
def register_module_help_providers():
    """Register all module-specific help providers."""
    
    # Address Object module
    help_registry.register_module_help_provider(
        "scm_cli.cli.object.address_object.help",
        "AddressObjectHelp"
    )
    
    # Add more modules as they're created
    # help_registry.register_module_help_provider(
    #     "scm_cli.cli.object.address_group.help",
    #     "AddressGroupHelp"
    # )


# Initialize help content
register_core_help_content()
register_module_help_providers()