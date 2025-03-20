#!/usr/bin/env python3

from pathlib import Path


def fix_remaining_issues():
    """Fix the remaining type issues in the CLI by directly editing the file."""
    # 1. Fix cli.py issues
    cli_path = Path('src/mactime/cli.py')
    content = cli_path.read_text()
    
    # Replace problematic TypedDict key accesses with string keys
    content = content.replace('paths[str(file)][OPENED_NAME]', 'paths[str(file)][str(OPENED_NAME)]')
    content = content.replace('source_attrs[name]', 'source_attrs[str(name)]')
    content = content.replace('result = {path: {name: value}', 'result = {str(path): {str(name): value}')
    
    cli_path.write_text(content)
    print(f"Fixed remaining issues in {cli_path}")
    
    # 2. Fix any unresolved issues in utils.py
    utils_path = Path('src/mactime/utils.py')
    content = utils_path.read_text()
    
    # Make sure we're using str instead of tuples
    content = content.replace('rows[0].append((header, "center"))', 'rows[0].append(str(header))')
    
    utils_path.write_text(content)
    print(f"Fixed remaining issues in {utils_path}")


if __name__ == "__main__":
    fix_remaining_issues()
