#!/usr/bin/env python3

from pathlib import Path
import re


def fix_syntax_cli():
    file_path = Path('src/mactime/cli.py')
    content = file_path.read_text()
    
    # Fix the unterminated string literal
    content = re.sub(
        r'help="Allowed values described above\.
"',
        'help="Allowed values described above.\\n"',
        content
    )
    
    content = re.sub(
        r'"This attribute is updated to current system time whenever some attributes are changed\.
"',
        '"This attribute is updated to current system time whenever some attributes are changed.\\n"',
        content
    )
    
    file_path.write_text(content)
    print(f"Fixed syntax issues in {file_path}")


if __name__ == "__main__":
    fix_syntax_cli()
