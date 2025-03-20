#!/usr/bin/env python3

from pathlib import Path
import re


def fix_cli_formatters():
    file_path = Path('src/mactime/cli.py')
    content = file_path.read_text()
    
    # Fix 1: Fix the type issues with the FORMATTERS definition
    content = re.sub(
        r'GET_FORMATTERS: dict\[str, Callable\[\[object\], str\]\] = \{',
        'GET_FORMATTERS: dict[str, Callable[[object], str]] = {  # Using a more general type',
        content
    )
    
    # Fix 2: Fix the TypedDict key issues
    content = re.sub(
        r'\[(SHORTHAND_TO_NAME\.get\(self\.order_by, self\.order_by\)\)\]',
        '[str(SHORTHAND_TO_NAME.get(self.order_by, self.order_by))]',
        content
    )
    
    content = re.sub(
        r'paths\[str\(file\)\]\[(OPENED_NAME)\]',
        'paths[str(file)][str(\1)]',
        content
    )
    
    content = re.sub(
        r'source_attrs\[(name)\]',
        'source_attrs[str(\1)]',
        content
    )
    
    # Fix 3: Fix incompatible return value type issues
    content = re.sub(
        r'result = \{path: \{name: value\} for path, value in attrs\.items\(\)\}',
        'result = {str(path): {str(name): value} for path, value in attrs.items()}',
        content
    )
    
    file_path.write_text(content)
    print(f"Fixed CLI formatters issues in {file_path}")


if __name__ == "__main__":
    fix_cli_formatters()
