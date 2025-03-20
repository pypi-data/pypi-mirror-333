#!/usr/bin/env python3

import re
from pathlib import Path


def fix_cli_py():
    cli_path = Path('../src/mactime/cli.py')
    if not cli_path.exists():
        cli_path = Path('src/mactime/cli.py')
    
    content = cli_path.read_text()
    
    # Add imports if needed
    content = re.sub(
        r'from typing import ',
        'from typing import Callable, Mapping, Sequence, cast, ',
        content
    )
    
    # Fix the FORMATTERS type annotation
    content = re.sub(
        r'FORMATTERS: dict\[str, .*?\] = \{',
        'FORMATTERS: dict[str, Callable[[Mapping[str, object]], str]] = {',
        content
    )
    
    # Fix Get.__call__ return type
    content = re.sub(
        r'def __call__\(self\) -> dict\[str, .*?\]:',
        'def __call__(self) -> int:  # Fixed return type to match parent class',
        content
    )
    
    # Add return statement at the end of Get.__call__
    content = re.sub(
        r'return \w+',
        'print(self.FORMATTERS[self.format](result))\n        return 0',
        content
    )
    
    # Fix the type for get_last_opened_dates
    content = re.sub(
        r'opened = get_last_opened_dates\(list\(paths\)\)',
        'opened = get_last_opened_dates(cast(list[PathType], list(paths)))',
        content
    )
    
    # Fix Match.__call__ and Reset.__call__ return types
    content = re.sub(
        r'(def __call__\(self\))( -> None)?:',
        '\\1 -> int:',
        content
    )
    
    # Add return 0 at the end of methods that need it
    content = content.replace(
        "modify_macos_times(path, to_set, no_follow=self.no_follow)",
        "modify_macos_times(path, to_set, no_follow=self.no_follow)\n        return 0"
    )
    
    # Write changes to file
    cli_path.write_text(content)
    print(f"Fixed CLI type issues in {cli_path}")


if __name__ == "__main__":
    fix_cli_py()
