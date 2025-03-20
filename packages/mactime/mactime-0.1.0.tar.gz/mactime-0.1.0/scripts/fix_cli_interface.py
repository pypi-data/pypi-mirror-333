#!/usr/bin/env python3

import re
from pathlib import Path


def fix_cli_interface():
    file_path = Path('src/mactime/_cli_interface.py')
    
    content = file_path.read_text()
    
    # Fix 1: Fix the incompatible types in assignment
    content = re.sub(
        r'if annotation == "bool" and "action" not in metadata:',
        'if str(annotation) == "bool" and "action" not in metadata:',
        content
    )
    
    # Fix 2: Add type annotation for annotations variable
    content = re.sub(
        r'annotations = \{\}',
        'annotations: dict[str, object] = {}',
        content
    )
    
    # Fix 3: Fix cleandoc with potential None
    content = re.sub(
        r'doc = cleandoc\(command_cls\.__doc__\)',
        'doc = cleandoc(command_cls.__doc__ or "")',
        content
    )
    
    # Fix 4: Fix _active_parser attribute error
    content = re.sub(
        r'command_cls\._active_parser = subparser',
        'setattr(command_cls, "_active_parser", subparser)  # use setattr to avoid mypy error',
        content
    )
    
    file_path.write_text(content)
    print(f"Fixed CLI interface issues in {file_path}")


if __name__ == "__main__":
    fix_cli_interface()
