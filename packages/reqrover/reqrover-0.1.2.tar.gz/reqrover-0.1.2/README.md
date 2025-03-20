# Req-Rover

A tool for discovering Python package dependencies in your project.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Basic usage - analyze current directory
rover

# Analyze a specific path
rover /path/to/project

# Output dependencies to a file
rover -o requirements.txt

# Show dependency tree
rover --tree

# Combine options
rover /path/to/project -o requirements.txt --tree
```

## Features

- Detects imported packages in Python files
- Generates requirements file
- Shows dependency tree visualization
- Attempts to detect and exclude local package from requirements
