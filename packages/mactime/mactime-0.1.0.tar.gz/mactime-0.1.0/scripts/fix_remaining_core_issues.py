#!/usr/bin/env python3

from pathlib import Path
import re


def fix_core_issues():
    file_path = Path('src/mactime/core.py')
    content = file_path.read_text()
    
    # Fix 1: Add type annotation for attr_map in set_timespec_attrs function
    content = re.sub(
        r'def set_timespec_attrs\(\s*path: PathType,\s*attr_map: dict\[int, Timespec\],',
        'def set_timespec_attrs(\n    path: PathType, attr_map: dict[int, Timespec],',
        content
    )
    
    # Fix 2: Fix the TimeSpecAttrs return type in get_timespec_attrs
    content = re.sub(
        r'return result',
        'return cast(TimeSpecAttrs, result)',
        content
    )
    
    # Fix 3: Fix the TypedDict key issues with string literals
    content = re.sub(
        r'(attr_map\[attr\])',
        r'attr_map[int(attr)]',
        content
    )
    
    # Make sure it imports cast
    if 'from typing import cast' not in content and 'cast,' not in content:
        content = re.sub(
            r'from typing import TYPE_CHECKING, TypedDict',
            'from typing import TYPE_CHECKING, TypedDict, cast',
            content
        )
    
    file_path.write_text(content)
    print(f"Fixed remaining core issues in {file_path}")


if __name__ == "__main__":
    fix_core_issues()
