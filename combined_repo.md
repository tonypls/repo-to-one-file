# Directory Structure

```
repo-to-one-file/
  README.md
  setup.py
  .pytest_cache/
    README.md
    v/
  repo-to-one-file/
    __init__.py
    __main__.py
  tests/
  repo_to_one_file.egg-info/
```

## README.md

````md
# repo-to-one-file

repo-to-one-file is a Python tool that consolidates repository files into a single Markdown file. It's designed to create a comprehensive overview of a codebase, which can be particularly useful for documentation or as context for large language models.

## Features

- Generates a directory structure of the repository
- Consolidates content of specified file types (.py, .js, .ts, .json, etc.) into a single Markdown file
- Ignores common non-source files and directories (node_modules, .git, etc.)
- Configurable maximum line count per file
- Option to include normally ignored files

## Installation

You can install repo-to-one-file directly from GitHub:

```bash
pip install git+https://github.com/tonypls/repo-to-one-file.git
```
````

````

## .pytest_cache/README.md

```md
# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.

````

## setup.py

```py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="repo-to-one-file",
    version="1.0.1",
    author="Tonypls",
    author_email="tony@appy.co.nz",
    description="A tool to consolidate repository files into a single file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tonypls/repo-to-one-file",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        # List your project dependencies here
    ],
    entry_points={
    "console_scripts": [
        "repo-to-one-file=repo_to_one_file.__main__:main",
    ],
},
)
```

## repo-to-one-file/**init**.py

```py
from .__main__ import create_markdown, generate_directory_structure

__version__ = "1.0.1"
__all__ = ['create_markdown', 'generate_directory_structure']

"""
repo-to-one-file: A tool to consolidate repository files into a single Markdown file.

This package provides functionality to:
1. Generate a directory structure of a given repository
2. Create a consolidated Markdown file of the repository contents
"""
```

## repo-to-one-file/**main**.py

````py
import os
import argparse
import fnmatch

def read_file_content(file_path, max_lines):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if len(lines) > max_lines:
                return f"File exceeds {max_lines} lines. Skipped."
            return ''.join(lines)
    except Exception as e:
        return f"Error reading file: {str(e)}"

def get_language(file_path):
    extension = os.path.splitext(file_path)[1][1:]
    return extension if extension else 'text'

def should_include(filename, relative_path, ignored_patterns):
    if any(fnmatch.fnmatch(relative_path, pattern) for pattern in ignored_patterns):
        return False
    return (filename.lower() == 'readme.md' or
            filename in ['package.json', 'requirements.txt', 'pyproject.toml'] or
            filename.endswith('.py') or
            filename.endswith('.js') or filename.endswith('.jsx') or
            filename.endswith('.ts') or filename.endswith('.tsx') or
            filename.endswith('.json'))

def generate_directory_structure(repo_path, ignored_patterns):
    structure = []
    for root, dirs, files in os.walk(repo_path):
        level = root.replace(repo_path, '').count(os.sep)
        indent = '  ' * level
        folder_name = os.path.basename(root)
        structure.append(f'{indent}{folder_name}/')

        subindent = '  ' * (level + 1)
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), repo_path)
            if should_include(file, relative_path, ignored_patterns):
                structure.append(f'{subindent}{file}')

        # Prune ignored directories
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignored_patterns)]

    return '\n'.join(structure)

def create_markdown(repo_path, output_file, max_lines, ignored_patterns):
    with open(output_file, 'w', encoding='utf-8') as out_file:
        # Add directory structure
        out_file.write("# Directory Structure\n\n```\n")
        out_file.write(generate_directory_structure(repo_path, ignored_patterns))
        out_file.write("\n```\n\n")

        # First, add README, package.json, or equivalent
        priority_files = ['readme.md', 'package.json', 'requirements.txt', 'pyproject.toml']
        for root, _, files in os.walk(repo_path):
            for file in sorted(files):
                relative_path = os.path.relpath(os.path.join(root, file), repo_path)
                if file.lower() in priority_files and should_include(file, relative_path, ignored_patterns):
                    file_path = os.path.join(root, file)
                    content = read_file_content(file_path, max_lines)
                    language = get_language(file_path)
                    out_file.write(f"## {relative_path}\n\n```{language}\n{content}\n```\n\n")

        # Then, add all .py, .js*, .ts*, and .json files
        for root, _, files in os.walk(repo_path):
            for file in sorted(files):
                relative_path = os.path.relpath(os.path.join(root, file), repo_path)
                if should_include(file, relative_path, ignored_patterns) and file.lower() not in priority_files:
                    file_path = os.path.join(root, file)
                    content = read_file_content(file_path, max_lines)
                    language = get_language(file_path)
                    out_file.write(f"## {relative_path}\n\n```{language}\n{content}\n```\n\n")

def main():
    parser = argparse.ArgumentParser(description="Consolidate repository files into a single Markdown file.")
    parser.add_argument("--max-lines", type=int, default=1000, help="Maximum number of lines per file (default: 1000)")
    parser.add_argument("--include-ignored", action="store_true", help="Include files that would normally be ignored")

    args = parser.parse_args()

    repo_path = os.getcwd()
    output_file = "combined_repo.md"

    ignored_patterns = [
    "node_modules*", "package-lock.json", "npm-debug.log", "yarn.lock", "yarn-error.log",
    "pnpm-lock.yaml", "bun.lockb", "deno.lock", "vendor", "composer.lock",
    "__pycache__", "*.pyc", "*.pyo", "*.pyd", ".Python", "pip-log.txt",
    "pip-delete-this-directory.txt", ".venv", "venv", "ENV", "env",
    "Gemfile.lock", ".bundle", "target", "*.class", ".gradle", "build",
    "pom.xml.tag", "pom.xml.releaseBackup", "pom.xml.versionsBackup", "pom.xml.next",
    "bin", "obj", "*.suo", "*.user", "go.sum", "Cargo.lock",
    ".git", ".svn", ".hg", ".DS_Store", "Thumbs.db",
    ".env", ".env.local", ".env.development.local", ".env.test.local", ".env.production.local",
    "*.env", "*.env.*", ".svelte-kit", ".next", ".nuxt", ".vuepress", ".cache", "dist", "tmp",
    "cache*", "venv*", ".expo*",
    # Additional common files to ignore
    "*.com", "*.dll", "*.exe", "*.o", "*.so",
    # Packages
    "*.7z", "*.dmg", "*.gz", "*.iso", "*.jar", "*.rar", "*.tar", "*.zip",
    # Logs and databases
    "*.log", "*.sql", "*.sqlite",
    # OS generated files
    ".DS_Store?", "._*", ".Spotlight-V100", ".Trashes", "ehthumbs.db"
]

    if args.include_ignored:
        ignored_patterns = []

    create_markdown(repo_path, output_file, args.max_lines, ignored_patterns)
    print(f"Markdown file created: {output_file}")

if __name__ == "__main__":
    main()
````
