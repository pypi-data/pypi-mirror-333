# Import Guidelines for pan-scm-cli

This document outlines the import patterns and best practices for the pan-scm-cli project to ensure consistent, maintainable, and production-ready code that works properly when the package is installed and distributed.

## Import Structure Overview

Our import structure follows a clear hierarchy with three distinct groups:

1. **Standard Library Imports**
   - Python's built-in modules (e.g., `os`, `sys`, `typing`, etc.)
   - Always placed at the top of the file

2. **Third-party Library Imports**
   - External dependencies (e.g., `cmd2`, `rich`, `pydantic`, etc.)
   - Placed after standard library imports

3. **Local Package Imports**
   - Imports from the `scm_cli` package and its modules
   - Placed after third-party imports
   - **IMPORTANT**: Use `scm_cli` as the root package, not `src.scm_cli` (see below)

Each group should be separated by a blank line, and imports within each group should be sorted alphabetically.

## Import Patterns

### 1. Absolute vs. Relative Imports

For importing within the package, we follow these guidelines:

#### Use Absolute Imports for:

- Importing modules from different parts of the package that aren't directly related:

```python
# Good
from scm_cli.utils.config import load_oauth_credentials
from scm_cli.utils.decorators import timeit

# BAD - DO NOT USE src prefix in imports!
from src.scm_cli.utils.config import load_oauth_credentials  # BAD!
```

#### Use Relative Imports for:

- Closely related modules within the same package/subpackage:

```python
# Good - importing from a sibling module
from .models import AddressObjectAPI

# Good - importing from a parent package
from .. import common_module
```

### 2. Common Patterns to Follow

#### Multiple Imports from the Same Module

When importing multiple items from the same module, use parentheses for clarity:

```python
from typing import (
    Dict, 
    List, 
    Optional, 
    Any, 
    Tuple,
)
```

#### Import Aliases

Use import aliases when there might be name conflicts or for clarity:

```python
import pandas as pd
from scm_cli.utils.decorators import timeit as measure_execution_time
```

### 3. Avoiding Common Problems

#### Import Path Issues

A common issue occurs when using `src.scm_cli` in import paths, which works during development but fails when the package is installed. Always use `scm_cli` as the root package name:

```python
# BAD - Will break when package is installed
from src.scm_cli.utils.config import load_config  # BAD!

# GOOD - Works both in development and after installation
from scm_cli.utils.config import load_config
```

#### Circular Imports

Avoid circular imports by:
1. Moving shared functionality to a common parent module
2. Using import statements within functions where needed
3. Using type hints with string references (`'Type'` instead of `Type`) when necessary

```python
# Instead of this (potentially circular)
from scm_cli.models.user import User

# Use this within a function if needed
def process_user(user_id):
    from scm_cli.models.user import User
    user = User.get(user_id)
    # ...
```

#### Wildcard Imports

Avoid wildcard imports (`from module import *`) as they make it unclear which names are being used:

```python
# BAD
from scm_cli.utils.constants import *  # BAD!

# GOOD
from scm_cli.utils.constants import (
    DEFAULT_TIMEOUT, 
    MAX_RETRIES,
    API_VERSION,
)
```

## Development vs. Installed Package Imports

In Poetry projects with `src/` layout, there's an important difference between development mode and installed package imports:

1. **Development Mode**: 
   - When running code from the project directory, the `src/` directory is part of the path.
   - IMPORTANT: Even in development, never use `src.scm_cli` in imports.

2. **Installed Package**:
   - When the package is installed with pip or poetry, the package's root is `scm_cli`, not `src.scm_cli`.
   - All imports must use `scm_cli` as the root.

Poetry handles the mapping between development and installed modes through the `pyproject.toml` configuration:

```toml
[tool.poetry]
packages = [{include = "scm_cli", from = "src"}]
```

## Why These Guidelines Matter

Following these import guidelines ensures:

1. **Consistency**: Makes the codebase more readable and maintainable
2. **Installation Compatibility**: Ensures the package works correctly when installed
3. **Distribution Readiness**: Makes the package ready for PyPI distribution
4. **Refactoring Safety**: Makes refactoring easier and safer

## Examples

### Good Import Organization

```python
# Standard library imports
import logging
import re
from typing import Dict, List, Optional

# Third-party imports
from pydantic import BaseModel
from rich.console import Console
from scm.client import ScmClient

# Local package imports
from scm_cli.utils.config import load_oauth_credentials
from scm_cli.utils.decorators import timeit, retry
from .models import AddressObjectAPI
```

### Bad Import Organization (Don't Do This)

```python
# BAD - Mixed imports, no grouping, src prefix
import re
from src.scm_cli.utils.config import load_oauth_credentials  # BAD!
from rich.console import Console
from .models import AddressObjectAPI
import logging
from pydantic import BaseModel
from typing import Dict, List, Optional
from src.scm_cli.utils.decorators import timeit, retry  # BAD!
from scm.client import ScmClient
```

## Conclusion

Consistent import practices are critical for maintainable code and successful package distribution. Always use the package name (`scm_cli`) without the `src` prefix in imports, and follow the grouping and organization patterns outlined in this document.