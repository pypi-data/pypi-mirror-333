#!/usr/bin/env python3

from pathlib import Path
import re


def fix_cli_interface2():
    file_path = Path('src/mactime/_cli_interface.py')
    content = file_path.read_text()
    
    # Fix 1: Fix the incompatible types in assignment for field_default
    content = re.sub(
        r'if field_default is not dataclasses\.MISSING:\s+default = field_default',
        'if field_default is not dataclasses.MISSING:\n        # Convert to appropriate type for assignment compatibility\n        if isinstance(field_default, (str, type(None))):\n            default = field_default\n        else:\n            default = str(field_default)',
        content
    )
    
    # Fix 2: Fix the issue with choices - make sure it's properly converted
    content = re.sub(
        r'if choices is not None:\s+metadata\["choices"\] = choices',
        'if choices is not None:\n        # Convert to list to fix type compatibility\n        metadata["choices"] = list(choices) if not isinstance(choices, list) else choices',
        content
    )
    
    file_path.write_text(content)
    print(f"Fixed additional CLI interface issues in {file_path}")


if __name__ == "__main__":
    fix_cli_interface2()
