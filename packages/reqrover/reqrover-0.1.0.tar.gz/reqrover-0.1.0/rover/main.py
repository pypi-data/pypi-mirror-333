import os
import ast
import importlib.util
import sys
from typing import Set, List, Dict, Optional, Tuple

def extract_imports_from_file(file_path: str) -> Set[str]:
    """
    Extracts imported package names from a Python file.
    
    Parameters:
        file_path (str): Path to the Python file.
        
    Returns:
        Set[str]: Set of unique package names.
    """
    packages = set()
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    packages.add(alias.name.split(".")[0])  # Get top-level package
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    packages.add(node.module.split(".")[0])  # Get top-level package

    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Skipping {file_path} due to error: {e}")
    
    return packages

def find_python_files(directory: str) -> List[str]:
    """
    Recursively finds all .py files in a directory.
    
    Parameters:
        directory (str): Root directory to search for Python files.
        
    Returns:
        List[str]: List of Python file paths.
    """
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files

def extract_imports_from_directory(directory: str) -> Set[str]:
    """
    Extracts all unique imported packages from Python files in a directory.
    
    Parameters:
        directory (str): Directory to search.
        
    Returns:
        Set[str]: Set of unique package names.
    """
    all_packages = set()
    python_files = find_python_files(directory)

    for file in python_files:
        all_packages.update(extract_imports_from_file(file))
    
    return all_packages

def get_local_package_name(directory: str) -> Optional[str]:
    """
    Try to find the local package name from setup.py or pyproject.toml.
    
    Parameters:
        directory (str): Project directory.
        
    Returns:
        Optional[str]: Package name if found, None otherwise.
    """
    # Check pyproject.toml
    pyproject_path = os.path.join(directory, "pyproject.toml")
    if os.path.exists(pyproject_path):
        try:
            with open(pyproject_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Very simple parsing - would be better with a proper TOML parser
                if 'name = "' in content:
                    name_line = [line for line in content.split("\n") if 'name = "' in line][0]
                    return name_line.split('name = "')[1].split('"')[0]
        except Exception as e:
            print(f"Error reading pyproject.toml: {e}")
    
    # Check setup.py
    setup_path = os.path.join(directory, "setup.py")
    if os.path.exists(setup_path):
        try:
            with open(setup_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Simple parsing - not comprehensive
                if "name=" in content:
                    name_line = [line for line in content.split("\n") if "name=" in line][0]
                    # Extract value between quotes
                    import re
                    match = re.search(r'name=["\']([^"\']+)["\']', name_line)
                    if match:
                        return match.group(1)
        except Exception as e:
            print(f"Error reading setup.py: {e}")
    
    return None

def build_dependency_tree(directory: str) -> Dict[str, Set[str]]:
    """
    Build a dependency tree showing which file imports which package.
    
    Parameters:
        directory (str): Directory to search.
        
    Returns:
        Dict[str, Set[str]]: Mapping of file paths to sets of imported packages.
    """
    dependency_tree = {}
    python_files = find_python_files(directory)

    for file in python_files:
        packages = extract_imports_from_file(file)
        if packages:  # Only include files with imports
            # Make path relative to the directory
            rel_path = os.path.relpath(file, directory)
            dependency_tree[rel_path] = packages
    
    return dependency_tree

def display_dependency_tree(tree: Dict[str, Set[str]]) -> None:
    """
    Display a formatted dependency tree.
    
    Parameters:
        tree (Dict[str, Set[str]]): Dependency tree to display.
    """
    print("\nDependency Tree:")
    print("---------------")
    
    for file_path, packages in sorted(tree.items()):
        print(f"\n{file_path}")
        for package in sorted(packages):
            print(f"  └── {package}")

def generate_requirements_file(packages: Set[str], output_path: str) -> None:
    """
    Generate a requirements file from the set of packages.
    
    Parameters:
        packages (Set[str]): Set of package names.
        output_path (str): Path where the requirements file should be saved.
    """
    # Filter out standard library packages
    std_lib = set(sys.builtin_module_names)
    
    # Check if a module is part of the standard library
    non_std_packages = set()
    for package in packages:
        spec = importlib.util.find_spec(package)
        if spec is None or (spec.origin is not None and 'site-packages' in spec.origin):
            non_std_packages.add(package)
    
    # Write requirements file
    with open(output_path, "w", encoding="utf-8") as f:
        for package in sorted(non_std_packages):
            f.write(f"{package}\n")
    
    print(f"Requirements written to {output_path}")

# If this file is run directly, use default behavior
if __name__ == "__main__":
    target_directory = "."  # Change to your project directory
    packages = extract_imports_from_directory(target_directory)
    print("\nDetected packages:")
    for package in sorted(packages):
        print(package)