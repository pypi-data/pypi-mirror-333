# SCM CLI Help System

The SCM CLI provides a robust help system to assist users in understanding and using commands effectively. This document explains how to use the help system and how to extend it with new command documentation.

## Features

The help system offers these features:

- **Rich Formatted Tables**: Using Rich's Table component with rounded borders for beautiful output
- **Contextual Help**: Different formatting for commands, arguments, options, and examples
- **Modular Design**: Help content organized by module for easier maintenance
- **Consistent Style**: Unified styling across all help content
- **Multiple Access Methods**: Both `help` command and `--help` flag support

## Using the Help System

There are two primary ways to access help in the SCM CLI:

1. The `help` command
2. The `--help` flag

### Using the `help` Command

The `help` command provides information about commands and their usage:

1. **General Help**:
   ```
   developer@scm> help
   ```
   This displays a list of all available commands with brief descriptions, organized by categories.

2. **Command-Specific Help**:
   ```
   developer@scm> help set
   ```
   This displays detailed help for the `set` command, including description, available subcommands, and examples.

3. **Subcommand Help**:
   ```
   developer@scm> help set address-object
   ```
   This shows help for the specific `set address-object` subcommand.

### Using the `--help` Flag

The `--help` flag can be appended to any command to get context-specific help:

1. **Command Help**:
   ```
   developer@scm> set --help
   ```
   This displays help for the `set` command, including available subcommands.

2. **Subcommand Help**:
   ```
   developer@scm> set address-object --help
   ```
   This displays detailed help for the `set address-object` subcommand, including required and optional arguments, examples, and usage notes.

### When to Use Each Method

- **Use `--help` flag** when you're already typing a command and want help with that specific command or subcommand
- **Use `help <command>`** when you want to explore what commands are available or learn about a command you're not currently using

## Help Content Structure

Help content is organized hierarchically:

1. **Commands** - Top-level commands like `set`, `show`, `delete`, etc.
2. **Subcommands** - Command-specific operations like `set address-object`, `show address-object`, etc.
3. **Arguments and Options** - Parameters for commands and subcommands.

For each command and subcommand, the help system provides:

- **Description** - Brief explanation of the command's purpose
- **Required Arguments** - Arguments that must be provided
- **Optional Arguments** - Arguments that can be omitted
- **Examples** - Usage examples demonstrating common operations
- **Notes** - Additional information and tips

## Examples

### Getting Help with the `help` Command

```
developer@scm> help
```

This displays all available commands organized by categories:

```
         Configuration Commands          
╭───────────┬───────────────────────────╮
│ Command   │ Description               │
├───────────┼───────────────────────────┤
│ configure │ Enter configuration mode. │
│ edit      │ Edit a specific folder.   │
╰───────────┴───────────────────────────╯
         Address Object Commands         
╭─────────┬─────────────────────────────╮
│ Command │ Description                 │
├─────────┼─────────────────────────────┤
│ delete  │ Delete an object.           │
│ set     │ Set an object's properties. │
│ show    │ Show object details.        │
╰─────────┴─────────────────────────────╯
               General Commands                
╭─────────┬───────────────────────────────────╮
│ Command │ Description                       │
├─────────┼───────────────────────────────────┤
│ exit    │ Exit the current mode or the CLI. │
│ quit    │ Exit the CLI.                     │
╰─────────┴───────────────────────────────────╯
         History Commands          
╭─────────┬───────────────────────╮
│ Command │ Description           │
├─────────┼───────────────────────┤
│ history │ Show command history. │
╰─────────┴───────────────────────╯
           System Commands           
╭─────────┬─────────────────────────╮
│ Command │ Description             │
├─────────┼─────────────────────────┤
│ logger  │ Control logging levels. │
╰─────────┴─────────────────────────╯
       Cache Management Commands        
╭─────────┬────────────────────────────╮
│ Command │ Description                │
├─────────┼────────────────────────────┤
│ cache   │ Manage API response cache. │
╰─────────┴────────────────────────────╯
            Uncategorized             
╭─────────┬──────────────────────────╮
│ Command │ Description              │
├─────────┼──────────────────────────┤
│ help    │ Show help for a command. │
╰─────────┴──────────────────────────╯

Use 'help <command>' or '<command> --help' for more information about a specific command.
```

### Getting Help for the `set` Command Using Both Methods

#### Using `help set`:

```
developer@scm> help set
```

Output:
```
## set ##

Set (create or update) object properties

                                    Examples                                    
╭────────────────────────────────────────────────┬─────────────────────────────╮
│ Example                                        │ Description                 │
├────────────────────────────────────────────────┼─────────────────────────────┤
│ set address-object name webserver1 type        │ Create a new address object │
│ ip-netmask value 192.168.1.1/32                │                             │
╰────────────────────────────────────────────────┴─────────────────────────────╯

Notes:
1. The set command is used to create new objects or update existing ones.
2. For existing objects, you can perform partial updates by specifying only the 
fields you want to change.

               Available Set Subcommands               
╭────────────────┬────────────────────────────────────╮
│ Command        │ Description                        │
├────────────────┼────────────────────────────────────┤
│ address-object │ Create or update an address object │
╰────────────────┴────────────────────────────────────╯
```

#### Using `set --help`:

```
developer@scm> set --help
```

The output will be identical to using `help set`. Both methods provide the same formatted help content.

### Getting Help for Subcommands 

```
developer@scm> set address-object --help
```

Output:
```
## set address-object ##

Create or update an address object

                                        Required Arguments
╭───────────────┬────────────────────────────────────────────────────────────────────────────────╮
│ Argument      │ Description                                                                    │
├───────────────┼────────────────────────────────────────────────────────────────────────────────┤
│ <name>        │ Name of the address object                                                     │
│ type <type>   │ Type of address object (ip-netmask, ip-range, fqdn) - required for new objects │
│ value <value> │ Value of the address object - required for new objects                         │
╰───────────────┴────────────────────────────────────────────────────────────────────────────────╯
                    Optional Arguments
╭────────────────────┬───────────────────────────────────╮
│ Option             │ Description                       │
├────────────────────┼───────────────────────────────────┤
│ description <text> │ Description of the address object │
│ tags <tags>        │ Comma-separated list of tags      │
╰────────────────────┴───────────────────────────────────╯
                                                                            Examples
╭────────────────────────────────────────────────────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────╮
│ Example                                                                                                │ Description                                         │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ set address-object test1 type ip-netmask value 1.1.1.1/32                                              │ Create/update an IP address object                  │
│ set address-object test2 type fqdn value example.com                                                   │ Create/update a domain name address object          │
│ set address-object test3 type ip-range value 1.1.1.1-1.1.1.10 description "Test" tags "Automation,Web" │ Create/update an IP range with description and tags │
│ set address-object test1 description "Updated description"                                             │ Update just the description of an existing object   │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────╯

Notes:
1. For new objects, type and value are required.
2. For existing objects, you can update individual fields without specifying all fields.
3. Tags should be provided as a comma-separated list enclosed in quotes.
```

### Tips for Using Help

1. **Starting Point**: Use `help` with no arguments to see all available commands
2. **Exploring Options**: Use `help <command>` to learn about a specific command's options
3. **Context-Specific Help**: Use `--help` flag while typing a command to get help for that specific context
4. **Command Chain**: When using multi-part commands, apply `--help` to get help for the entire command chain

## Troubleshooting Help Issues

If you encounter issues with the help system, here are some common problems and solutions:

### Problem: Help Shows "No help available for: [command]"

This means the command doesn't have a registered help entry. Options:
1. Check your command spelling
2. Try using a simpler form of the command
3. Use `help` without arguments to see available commands

### Problem: Help Repeating or Recursion Errors

The help system is designed to prevent infinite recursion. If you see a message about "Help recursion detected", this is a safety feature to prevent the CLI from hanging.

### Problem: Incomplete Help Information

Some commands may have limited help content. You can:
1. Try using a different form of help (e.g., if `--help` doesn't show complete info, try `help command`)
2. Refer to the documentation or examples

## Best Practices for Using Help

1. **Start General, Then Get Specific**: Begin with `help` to see all commands, then drill down
2. **Use Tab Completion**: Many CLI commands support tab completion to show available options
3. **Combine with History**: Use the `history` command to see examples of previously used commands
4. **Try Both Methods**: Both `help <command>` and `<command> --help` provide similar information but in different contexts

## For Developers: Extending the Help System

The help system is designed to be easily extended with new command documentation. The preferred way to add help is through the module-specific help files as explained in the [Adding Help Content](adding_help.md) guide.

For direct registration, you can also use the `help_registry` module:

```python
from scm_cli.utils.help_formatter import help_registry

# Register help for a command
help_registry.register_command_help(
    command="my-command",
    description="Description of my command",
    required_args=[
        ("<arg1>", "Description of required argument 1"),
        ("<arg2>", "Description of required argument 2"),
    ],
    optional_args=[
        ("--option1", "Description of option 1"),
        ("--option2", "Description of option 2"),
    ],
    examples=[
        ("my-command arg1 arg2", "Example description"),
        ("my-command arg1 arg2 --option1", "Another example"),
    ],
    notes=[
        "Important note 1 about the command.",
        "Important note 2 about the command.",
    ]
)
```

This extensible approach makes it easy to maintain comprehensive, up-to-date documentation for all CLI commands.