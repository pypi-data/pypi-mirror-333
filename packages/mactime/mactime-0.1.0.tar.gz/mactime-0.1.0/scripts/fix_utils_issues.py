#!/usr/bin/env python3

from pathlib import Path
import re


def fix_utils_issues():
    file_path = Path('src/mactime/utils.py')
    content = file_path.read_text()
    
    # Fix 1: Fix the append issue with tuples
    content = re.sub(
        r'rows\[0\]\.append\(\(header, "center"\)\)',
        'rows[0].append(header)  # Fixed to use str instead of tuple',
        content
    )
    
    # Fix 2: Fix the function signature for generate_pretty_table
    content = re.sub(
        r'def generate_pretty_table\(headers: list\[str\], rows: list\[list\[str\]\]\) -> str:',
        'def generate_pretty_table(headers: list[str], rows: list[list[str | tuple[str, str]]]) -> str:',
        content
    )
    
    file_path.write_text(content)
    print(f"Fixed utils issues in {file_path}")


if __name__ == "__main__":
    fix_utils_issues()
