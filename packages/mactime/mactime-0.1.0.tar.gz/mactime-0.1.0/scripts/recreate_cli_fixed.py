#!/usr/bin/env python3

from pathlib import Path


def recreate_cli_fixed():
    """Create a fixed version of cli.py with properly escaped newlines"""
    file_path = Path('src/mactime/cli.py')
    
    # Get the current content
    content = file_path.read_text()
    
    # Fix escaped newlines
    content = content.replace('help="Allowed values described above.\n"', 'help="Allowed values described above.\\n"')
    content = content.replace('"This attribute is updated to current system time whenever some attributes are changed.\n"', '"This attribute is updated to current system time whenever some attributes are changed.\\n"')
    
    file_path.write_text(content)
    print(f"Fixed escape sequences in {file_path}")


if __name__ == "__main__":
    recreate_cli_fixed()
