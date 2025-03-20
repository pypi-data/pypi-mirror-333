#!/usr/bin/env python3

import re
from pathlib import Path


def fix_cli_syntax():
    file_path = Path('src/mactime/cli.py')
    
    content = file_path.read_text()
    
    # Fix the syntax error at line 379
    content = re.sub(
        r'print\(self\.FORMATTERS\[self\.format\]\(result\)\)\n        return 0\.fromkeys',
        'print(self.FORMATTERS[self.format](result))\n                return dict.fromkeys',
        content
    )
    
    file_path.write_text(content)
    print(f"Fixed syntax error in {file_path}")


if __name__ == "__main__":
    fix_cli_syntax()
