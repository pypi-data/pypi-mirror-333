"""Help content for address object commands."""

import logging
from typing import Dict, List, Tuple, Optional, Any

# Set up logger
logger = logging.getLogger("scm_cli.cli.object.address_object.help")


class AddressObjectHelp:
    """Help provider for address object commands."""
    
    # Set address-object command help
    @staticmethod
    def get_command_help(command: str) -> Optional[Dict[str, Any]]:
        """Get help for a command related to address objects.
        
        Args:
            command: Command name
            
        Returns:
            Dictionary with help content or None if not found
        """
        logger.debug(f"AddressObjectHelp.get_command_help called with: {command}")
        
        if command == "set":
            logger.debug("Returning help for 'set' command")
            return {
                "description": "Set (create or update) object properties",
                "examples": [
                    ("set address-object name webserver1 type ip-netmask value 192.168.1.1/32",
                     "Create a new address object")
                ],
                "notes": [
                    "The set command is used to create new objects or update existing ones.",
                    "For existing objects, you can perform partial updates by specifying only the fields you want to change."
                ],
                "required_args": [],
                "optional_args": []
            }
        elif command == "show":
            logger.debug("Returning help for 'show' command")
            return {
                "description": "Display object information",
                "examples": [
                    ("show address-object", "Show all address objects in current folder"),
                    ("show address-object webserver1", "Show details of a specific address object")
                ],
                "required_args": [],
                "optional_args": []
            }
        elif command == "delete":
            logger.debug("Returning help for 'delete' command")
            return {
                "description": "Delete objects",
                "examples": [
                    ("delete address-object webserver1", "Delete an address object")
                ],
                "notes": [
                    "Deletion is permanent and cannot be undone.",
                    "You must be in configuration mode to use this command."
                ],
                "required_args": [],
                "optional_args": []
            }
        
        logger.debug(f"No help found for command: {command}")
        return None
    
    @staticmethod
    def get_subcommand_help(command: str, subcommand: str) -> Optional[Dict[str, Any]]:
        """Get help for a subcommand related to address objects.
        
        Args:
            command: Parent command name
            subcommand: Subcommand name
            
        Returns:
            Dictionary with help content or None if not found
        """
        logger.debug(f"AddressObjectHelp.get_subcommand_help called with: {command} {subcommand}")
        
        if command == "set" and subcommand == "address-object":
            logger.debug("Returning help for 'set address-object' subcommand")
            return {
                "description": "Create or update an address object",
                "required_args": [
                    ("<name>", "Name of the address object"),
                    ("type <type>", "Type of address object (ip-netmask, ip-range, fqdn) - required for new objects"),
                    ("value <value>", "Value of the address object - required for new objects")
                ],
                "optional_args": [
                    ("description <text>", "Description of the address object"),
                    ("tags <tags>", "Comma-separated list of tags")
                ],
                "examples": [
                    ("set address-object test1 type ip-netmask value 1.1.1.1/32", 
                     "Create/update an IP address object"),
                    ("set address-object test2 type fqdn value example.com", 
                     "Create/update a domain name address object"),
                    ("set address-object test3 type ip-range value 1.1.1.1-1.1.1.10 description \"Test\" tags \"Automation,Web\"", 
                     "Create/update an IP range with description and tags"),
                    ("set address-object test1 description \"Updated description\"", 
                     "Update just the description of an existing object")
                ],
                "notes": [
                    "For new objects, type and value are required.",
                    "For existing objects, you can update individual fields without specifying all fields.",
                    "Tags should be provided as a comma-separated list enclosed in quotes."
                ]
            }
        elif command == "show" and subcommand == "address-object":
            logger.debug("Returning help for 'show address-object' subcommand")
            return {
                "description": "Display address object information",
                "required_args": [
                    ("[<name>]", "Optional name of a specific address object to show")
                ],
                "optional_args": [],
                "examples": [
                    ("show address-object", "List all address objects in current folder"),
                    ("show address-object webserver1", "Show details of the 'webserver1' address object")
                ],
                "notes": [
                    "Without a name parameter, shows all address objects in the current folder.",
                    "If a name is provided, shows detailed information for just that object."
                ]
            }
        elif command == "show" and subcommand == "address-objects-filter":
            logger.debug("Returning help for 'show address-objects-filter' subcommand")
            return {
                "description": "Search and filter address objects",
                "required_args": [],
                "optional_args": [
                    ("--name <name>", "Filter by object name (substring match)"),
                    ("--type <type>", "Filter by object type (ip-netmask, ip-range, fqdn)"),
                    ("--value <value>", "Filter by object value (substring match)"),
                    ("--tag <tag>", "Filter by tag (substring match)")
                ],
                "examples": [
                    ("show address-objects-filter --type ip-netmask", "Show all IP netmask objects"),
                    ("show address-objects-filter --name web --tag Production", "Show objects with 'web' in the name and 'Production' tag")
                ],
                "notes": [
                    "Multiple filters can be combined for more specific searches.",
                    "Filters perform substring matching, not exact matching."
                ]
            }
        elif command == "delete" and subcommand == "address-object":
            logger.debug("Returning help for 'delete address-object' subcommand")
            return {
                "description": "Delete an address object",
                "required_args": [
                    ("<name>", "Name of the address object to delete")
                ],
                "optional_args": [],
                "examples": [
                    ("delete address-object webserver1", "Delete the 'webserver1' address object")
                ],
                "notes": [
                    "You must be in folder edit mode to use this command.",
                    "Deletion is permanent and cannot be undone.",
                    "The object must exist in the current folder."
                ]
            }
            
        logger.debug(f"No help found for subcommand: {command} {subcommand}")
        return None
    
    @staticmethod
    def get_available_commands() -> List[Tuple[str, str]]:
        """Get list of available commands related to address objects.
        
        Returns:
            List of (command, description) tuples
        """
        logger.debug("AddressObjectHelp.get_available_commands called")
        
        # Return commands related to address objects
        # Note: Core commands like set/show/delete are registered in the central registry,
        # but we include them here for testing/completeness
        commands = [
            ("set", "Set (create or update) object properties"),
            ("show", "Display object information"),
            ("delete", "Delete objects")
        ]
        
        logger.debug(f"Returning commands: {commands}")
        return commands
    
    @staticmethod
    def get_available_subcommands(command: str) -> List[Tuple[str, str]]:
        """Get list of available subcommands for a command related to address objects.
        
        Args:
            command: Parent command name
            
        Returns:
            List of (subcommand, description) tuples
        """
        logger.debug(f"AddressObjectHelp.get_available_subcommands called with: {command}")
        
        if command == "set":
            logger.debug("Returning 'set' subcommands")
            return [
                ("address-object", "Create or update an address object")
            ]
        elif command == "show":
            logger.debug("Returning 'show' subcommands")
            return [
                ("address-object", "Display address object information"),
                ("address-objects-filter", "Search and filter address objects")
            ]
        elif command == "delete":
            logger.debug("Returning 'delete' subcommands")
            return [
                ("address-object", "Delete an address object")
            ]
            
        logger.debug(f"No subcommands found for: {command}")
        return []