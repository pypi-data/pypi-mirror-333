import os
import click
from typing import Optional
import importlib.util
import sys
import re
import tomli

from rover.main import (
    extract_imports_from_directory,
    get_local_package_name,
    build_dependency_tree,
    display_dependency_tree,
    generate_requirements_file
)

def get_current_package_name():
    """Determine the name of the package that contains this script."""
    # Try to find setup.py in parent directories
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Check for pyproject.toml
    pyproject_path = os.path.join(current_dir, "pyproject.toml")
    if os.path.exists(pyproject_path):
        try:
            with open(pyproject_path, "rb") as f:
                pyproject_data = tomli.load(f)
                if "project" in pyproject_data and "name" in pyproject_data["project"]:
                    return pyproject_data["project"]["name"]
        except Exception:
            pass
    
    # Check for setup.py
    setup_path = os.path.join(current_dir, "setup.py")
    if os.path.exists(setup_path):
        try:
            with open(setup_path, "r") as f:
                content = f.read()
                # Look for name="package_name" pattern
                match = re.search(r'name=[\'"]([^\'"]+)[\'"]', content)
                if match:
                    return match.group(1)
        except Exception:
            pass
    
    # If we couldn't determine the package name, return None
    return None

@click.command()
@click.argument('path', type=click.Path(exists=True), required=True)
@click.option('-o', '--output', type=click.Path(), help='Output requirements file path')
@click.option('--tree', is_flag=True, help='Display dependency tree')
def cli(path: str, output: Optional[str], tree: bool) -> None:
    """
    Analyze Python package imports in the specified directory.
    
    PATH is the directory to analyze.
    """
    # Get absolute path
    target_directory = os.path.abspath(path)
    
    print(f"Analyzing Python files in {target_directory}...")
    
    # Check if it's a package
    local_package = get_local_package_name(target_directory)
    if local_package:
        print(f"Detected local package: {local_package}")
    
    # Get the name of the current package (the one containing this script)
    current_package = get_current_package_name()
    
    # Get all packages
    packages = extract_imports_from_directory(target_directory)
    
    # Filter out standard library modules and local subpackages
    filtered_packages = []
    for package in packages:
        # Skip if it's the local package
        if local_package and (package == local_package or package.startswith(f"{local_package}.")):
            continue
        
        # Skip if it's the current package (the package containing this tool)
        if current_package and (package == current_package or package.startswith(f"{current_package}.")):
            continue
            
        # Add only top-level package names (before the first dot)
        top_level = package.split('.')[0]
        if top_level not in filtered_packages:
            filtered_packages.append(top_level)
    
    # Display packages
    print("\nDetected packages:")
    for package in sorted(filtered_packages):
        print(package)
    
    # Generate tree if requested
    if tree:
        dependency_tree = build_dependency_tree(target_directory)
        display_dependency_tree(dependency_tree)
    
    # Create requirements file if output path is provided
    if output:
        output_path = output
        generate_requirements_file(filtered_packages, output_path)
    elif filtered_packages:  # Default output file
        output_path = "used_dependencies.txt"
        generate_requirements_file(filtered_packages, output_path)

if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
