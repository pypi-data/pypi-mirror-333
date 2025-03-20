#!/usr/bin/env python3

import re
from pathlib import Path


def fix_errors():
    file_path = Path('src/mactime/errors.py')
    
    content = file_path.read_text()
    
    # Fix 1: Update constructor parameter type
    content = re.sub(
        r'def __init__\(\s*self,\s*path: str,',
        'def __init__(\n        self,\n        path: Union[str, PathLike[Any]],',
        content
    )
    
    # Fix 2: Update check_call parameter type
    content = re.sub(
        r'def check_call\(cls, ret: int, path: str \| os\.PathLike, operation: str\) -> None:',
        'def check_call(cls, ret: int, path: Union[str, PathLike[Any]], operation: str) -> None:',
        content
    )
    
    file_path.write_text(content)
    print(f"Fixed errors.py issues in {file_path}")


if __name__ == "__main__":
    fix_errors()
