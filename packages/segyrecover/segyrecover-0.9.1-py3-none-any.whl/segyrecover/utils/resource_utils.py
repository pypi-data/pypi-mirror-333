"""Utilities for managing application resources and tutorial files."""

import os
import shutil
import importlib.resources as pkg_resources
import importlib.util
import sys

def copy_tutorial_files(target_dir):
    """Copy tutorial files to the user's data directory."""
    # Create required folders if they don't exist
    folders = ['IMAGES', 'GEOMETRY', 'PARAMETERS']
    for folder in folders:
        folder_path = os.path.join(target_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
    
    try:
        # Determine if running from source or as an installed package
        package_name = 'segyrecover'
        examples_base = None
        
        # Method 1: Check if running from source
        module_path = getattr(sys.modules.get(package_name, None), '__file__', '')
        if module_path:
            source_dir = os.path.dirname(os.path.dirname(os.path.dirname(module_path)))
            examples_base = os.path.join(source_dir, 'examples')
            if os.path.exists(examples_base):
                print(f"Found examples directory at: {examples_base}")
        
        # Method 2: Look for examples in installed package
        if not examples_base or not os.path.exists(examples_base):
            try:
                # For Python 3.9+
                package_path = pkg_resources.files(package_name)
                if package_path:
                    examples_base = os.path.join(str(package_path), 'examples')
                    if not os.path.exists(examples_base):
                        examples_base = None
            except (ImportError, AttributeError):
                examples_base = None
                
        # Method 3: Look for examples in current directory or parent
        if not examples_base:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            for _ in range(3):  # Check up to 3 levels up
                test_path = os.path.join(current_dir, 'examples')
                if os.path.exists(test_path):
                    examples_base = test_path
                    break
                current_dir = os.path.dirname(current_dir)
                
        # Copy files if we found the examples
        if examples_base and os.path.exists(examples_base):
            print(f"Copying tutorial files from {examples_base}")
            for folder in folders:
                source_folder = os.path.join(examples_base, folder)
                if os.path.exists(source_folder):
                    for file in os.listdir(source_folder):
                        source = os.path.join(source_folder, file)
                        destination = os.path.join(target_dir, folder, file)
                        if os.path.isfile(source) and not os.path.exists(destination):
                            shutil.copy2(source, destination)
                            print(f"Copied {source} to {destination}")
        else:
            print("Could not find example files to copy")
                
    except Exception as e:
        print(f"Warning: Could not copy tutorial files: {e}")
