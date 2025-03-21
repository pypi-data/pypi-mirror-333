# Adding Help Content for Command Modules

This guide explains how to add help content for new command modules in the SCM CLI. Following this pattern ensures that help content is modular, maintainable, and correctly integrated with the `--help` flag system.

The SCM CLI uses Rich tables with rounded borders for beautiful, consistent help output. Help content is organized by module, making it easy to maintain as your module evolves.

## Creating a Help Module for Your Commands

Each command module should have its own help module that provides detailed help content. This keeps the help content close to the implementation and makes it easier to maintain.

### Step 1: Create a Help Module File

Create a `help.py` file in your command module directory. For example:

```
src/scm_cli/cli/object/my_module/help.py
```

### Step 2: Implement the Help Class

In your `help.py` file, implement a class that provides help content for your commands. The class should include these static methods:

```python
"""Help content for my module commands."""

from typing import Dict, List, Tuple, Optional, Any


class MyModuleHelp:
    """Help provider for my module commands."""
    
    @staticmethod
    def get_command_help(command: str) -> Optional[Dict[str, Any]]:
        """Get help for a command related to my module.
        
        Args:
            command: Command name
            
        Returns:
            Dictionary with help content or None if not found
        """
        if command == "my-command":
            return {
                "description": "Description of my command",
                "required_args": [
                    ("<arg1>", "Description of required argument 1"),
                    ("<arg2>", "Description of required argument 2"),
                ],
                "optional_args": [
                    ("--option1", "Description of option 1"),
                    ("--option2", "Description of option 2"),
                ],
                "examples": [
                    ("my-command arg1 arg2", "Example description"),
                    ("my-command arg1 arg2 --option1", "Another example"),
                ],
                "notes": [
                    "Important note 1 about the command.",
                    "Important note 2 about the command.",
                ]
            }
        
        return None
    
    @staticmethod
    def get_subcommand_help(command: str, subcommand: str) -> Optional[Dict[str, Any]]:
        """Get help for a subcommand related to my module.
        
        Args:
            command: Parent command name
            subcommand: Subcommand name
            
        Returns:
            Dictionary with help content or None if not found
        """
        if command == "my-command" and subcommand == "my-subcommand":
            return {
                "description": "Description of my subcommand",
                "required_args": [...],
                "optional_args": [...],
                "examples": [...],
                "notes": [...]
            }
            
        return None
    
    @staticmethod
    def get_available_commands() -> List[Tuple[str, str]]:
        """Get list of available commands related to my module.
        
        Returns:
            List of (command, description) tuples
        """
        return [
            ("my-command", "Description of my command"),
            # Add more commands as needed
        ]
    
    @staticmethod
    def get_available_subcommands(command: str) -> List[Tuple[str, str]]:
        """Get list of available subcommands for a command related to my module.
        
        Args:
            command: Parent command name
            
        Returns:
            List of (subcommand, description) tuples
        """
        if command == "my-command":
            return [
                ("my-subcommand", "Description of my subcommand"),
                # Add more subcommands as needed
            ]
            
        return []
```

### Step 3: Export the Help Class in `__init__.py`

Update your module's `__init__.py` to export the help class:

```python
"""My module commands for SCM CLI."""

from .commands import MyModuleCommands
from .help import MyModuleHelp
```

### Step 4: Register the Help Provider

In `src/scm_cli/utils/help_formatter.py`, find the `register_module_help_providers()` function and add your module:

```python
def register_module_help_providers():
    """Register all module-specific help providers."""
    
    # Existing providers
    help_registry.register_module_help_provider(
        "scm_cli.cli.object.address_object.help",
        "AddressObjectHelp"
    )
    
    # Add your module
    help_registry.register_module_help_provider(
        "scm_cli.cli.object.my_module.help",
        "MyModuleHelp"
    )
```

## Help Content Structure

Help content for commands and subcommands should follow this structure:

### For Commands

```python
{
    "description": "Brief description of what the command does",
    
    "required_args": [
        # List of required arguments as (name, description) tuples
        ("<arg1>", "Description of arg1"),
        ("<arg2>", "Description of arg2"),
    ],
    
    "optional_args": [
        # List of optional arguments as (name, description) tuples
        ("--option1", "Description of option1"),
        ("--option2", "Description of option2"),
    ],
    
    "examples": [
        # List of examples as (example, description) tuples
        ("command arg1 arg2", "Description of this example"),
        ("command arg1 arg2 --option1 value", "Description of this example"),
    ],
    
    "notes": [
        # List of additional notes as strings
        "Important note 1 about using this command.",
        "Important note 2 about using this command.",
    ]
}
```

### For Subcommands

Same structure as commands, but returned by the `get_subcommand_help` method for a specific command and subcommand combination.

## Best Practices

1. **Be Concise**: Keep descriptions brief but clear.
2. **Be Complete**: Include all required and optional arguments.
3. **Show Examples**: Provide practical examples of common use cases.
4. **Add Notes**: Include important notes, especially about constraints or side effects.
5. **Follow Style**: Maintain a consistent style with other help content.
6. **Keep Updated**: Update help content whenever the command implementation changes.

## Testing Help Content

To test your help content:
1. Start the CLI
2. Try `your-command --help` to view the command help
3. Try `your-command your-subcommand --help` to view subcommand help

If the help content doesn't appear, check:
1. That your help module is correctly registered
2. That your help class implements all required methods
3. That you're returning the correct data structure

## Example: AddressObjectHelp

Look at `src/scm_cli/cli/object/address_object/help.py` for a complete example of a help module.