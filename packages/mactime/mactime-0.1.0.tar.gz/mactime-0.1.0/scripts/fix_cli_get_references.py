#!/usr/bin/env python3

import re
from pathlib import Path


def fix_cli_get_references():
    file_path = Path('src/mactime/cli.py')
    
    content = file_path.read_text()
    
    # Fix 1: Create a variable for the result in Get.__call__
    content = re.sub(
        r'(def __call__\(self\) -> int:)',
        '\1\n        result = {}  # Define result variable',
        content
    )
    
    # Fix 2: Replace all Get.FORMATTERS with self.FORMATTERS in the Get class
    content = re.sub(
        r'Get\.FORMATTERS',
        'self.FORMATTERS',
        content
    )
    
    # Fix 3: Fix the missing return statements
    content = re.sub(
        r'(def reset_attr\(self, path: PathType, attr: str\) -> None:.*?)\n    \n    def ',
        '\1\n        return 0\n    \n    def ',
        content,
        flags=re.DOTALL
    )
    
    content = re.sub(
        r'(def match_items\(self, source: PathType, targets: list\[PathType\]\) -> None:.*?)\n    \n    def ',
        '\1\n        return 0\n    \n    def ',
        content,
        flags=re.DOTALL
    )
    
    file_path.write_text(content)
    print(f"Fixed Get references in {file_path}")


if __name__ == "__main__":
    fix_cli_get_references()
