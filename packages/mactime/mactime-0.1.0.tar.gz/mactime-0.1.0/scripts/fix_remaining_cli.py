#!/usr/bin/env python3

import re
from pathlib import Path


def fix_cli_specific():
    file_path = Path('src/mactime/cli.py')
    
    content = file_path.read_text()
    
    # Fix 1: Fix the return type annotation for Get.__call__
    content = re.sub(
        r'def __call__\(self\) -> int:  # Fixed return type to match parent class',
        'def __call__(self) -> int:',
        content
    )
    
    # Fix 2: Fixed the FORMATTERS references in the Get class and other places
    content = re.sub(
        r'print\(self\.FORMATTERS\[self\.format\]\(result\)\)',
        'print(Get.FORMATTERS[self.format](result))',
        content
    )
    
    # Fix 3: Fix the formatters definition
    content = re.sub(
        r'FORMATTERS: dict\[str, Callable\[\[Mapping\[str, object\]\], str\]\] = \{',
        'FORMATTERS: dict[str, Callable[[object], str]] = {',
        content
    )
    
    # Fix 4: Fix the missing return 0 for Set.__call__ and Match.__call__
    content = re.sub(
        r'(class Set\(Command\):.*?def __call__.*?\})\s*',
        '\1\n        return 0\n    ',
        content,
        flags=re.DOTALL
    )
    
    content = re.sub(
        r'(class Match\(Command\):.*?def __call__.*?\})\s*',
        '\1\n        return 0\n    ',
        content,
        flags=re.DOTALL
    )
    
    # Fix 5: Fix the type issues with get_last_opened_dates
    content = re.sub(
        r'opened = get_last_opened_dates\(cast\(list\[PathType\], list\(paths\)\)\)',
        'opened = get_last_opened_dates(cast(list[PathType], list(str(p) for p in paths)))',
        content
    )
    
    file_path.write_text(content)
    print(f"Fixed remaining CLI issues in {file_path}")


if __name__ == "__main__":
    fix_cli_specific()
