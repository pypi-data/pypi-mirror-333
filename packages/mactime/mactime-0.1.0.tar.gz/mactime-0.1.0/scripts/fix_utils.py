#!/usr/bin/env python3

import re
from pathlib import Path


def fix_utils():
    file_path = Path('src/mactime/utils.py')
    
    content = file_path.read_text()
    
    # Fix 1: Fix type issues with list.append
    content = re.sub(
        r'rows\[0\]\.append\(\(header, "center"\)\)',
        'rows[0].append(str(header))  # Modified to match expected type',
        content
    )
    
    # Fix 2: Update the generate_pretty_table type annotation
    content = re.sub(
        r'def generate_pretty_table\(headers: list\[str\], rows: list\[list\[str\]\]\) -> str:',
        'def generate_pretty_table(headers: list[str], rows: list[list[str | tuple[str, str]]]) -> str:',
        content
    )
    
    # Fix 3: Fix possibly unbound variable issues in utils.py
    content = re.sub(
        r'for i, width in enumerate\(widths\):',
        'i = 0  # Initialize i to avoid unbound variable issues\n        for i, width in enumerate(widths):',
        content
    )
    
    file_path.write_text(content)
    print(f"Fixed utils issues in {file_path}")


if __name__ == "__main__":
    fix_utils()
