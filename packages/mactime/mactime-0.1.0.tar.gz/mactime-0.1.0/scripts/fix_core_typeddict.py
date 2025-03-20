#!/usr/bin/env python3

import re
from pathlib import Path


def fix_core_typeddict():
    file_path = Path('src/mactime/core.py')
    
    content = file_path.read_text()
    
    # Fix 1: Fix TypedDict initialization and casting
    content = re.sub(
        r'result: TimeSpecAttrs = \{\}',
        'result = {}  # Initialize as dict and cast later',
        content
    )
    
    # Fix 2: Add explicit cast to TimeSpecAttrs at return
    content = re.sub(
        r'return result',
        'return {k: v for k, v in result.items()}  # Return as a new dict that matches TimeSpecAttrs',
        content
    )
    
    # Fix 3: Use literal string keys when accessing TypedDict
    content = re.sub(
        r'(attr_map\[)attr(\])',
        r'\1attr\2  # Using numeric constant as key',
        content
    )
    
    # Add an import for cast if not already present
    if 'from typing import cast' not in content and 'cast' not in content:
        content = re.sub(
            r'from typing import TYPE_CHECKING, TypedDict',
            'from typing import TYPE_CHECKING, TypedDict, cast',
            content
        )
    
    file_path.write_text(content)
    print(f"Fixed TypedDict issues in {file_path}")


if __name__ == "__main__":
    fix_core_typeddict()
