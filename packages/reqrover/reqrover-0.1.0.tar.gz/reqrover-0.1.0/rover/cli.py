import os
import click
from typing import Optional

from rover.main import (
    extract_imports_from_directory,
    get_local_package_name,
    build_dependency_tree,
    display_dependency_tree,
    generate_requirements_file
)

@click.command()
@click.argument('path', type=click.Path(exists=True), default=".")
@click.option('-o', '--output', type=click.Path(), help='Output requirements file path')
@click.option('--tree', is_flag=True, help='Display dependency tree')
def cli(path: str, output: Optional[str], tree: bool) -> None:
    """
    Analyze Python package imports in the specified directory.
    
    PATH is the directory to analyze (defaults to current directory).
    """
    # Get absolute path
    target_directory = os.path.abspath(path)
    
    print(f"Analyzing Python files in {target_directory}...")
    
    # Check if it's a package
    local_package = get_local_package_name(target_directory)
    if local_package:
        print(f"Detected local package: {local_package}")
    
    # Get all packages
    packages = extract_imports_from_directory(target_directory)
    
    # Remove local package from dependencies if found
    if local_package and local_package in packages:
        packages.remove(local_package)
    
    # Display packages
    print("\nDetected packages:")
    for package in sorted(packages):
        print(package)
    
    # Generate tree if requested
    if tree:
        dependency_tree = build_dependency_tree(target_directory)
        display_dependency_tree(dependency_tree)
    
    # Create requirements file if output path is provided
    if output:
        output_path = output
        generate_requirements_file(packages, output_path)
    elif packages:  # Default output file
        output_path = "used_dependencies.py"
        generate_requirements_file(packages, output_path)

if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
