"""Utility functions for handling resources."""
import os
import shutil
import pkg_resources

def copy_tutorial_files(target_dir):
    """
    Copy example files from the installed package to the user's data directory.
    
    Args:
        target_dir: The directory where files should be copied to
    """
    try:
        # Get the location of the example files in the installed package
        examples_dir = pkg_resources.resource_filename('segyrecover', 'examples')
        
        # If examples directory doesn't exist directly, try one level up
        if not os.path.exists(examples_dir):
            # Try to find examples in project root
            package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            examples_dir = os.path.join(os.path.dirname(package_dir), 'examples')
        
        if not os.path.exists(examples_dir):
            print(f"Examples directory not found: {examples_dir}")
            return
        
        # Copy example files to the corresponding directories in the target directory
        for root, dirs, files in os.walk(examples_dir):
            # Get relative path from examples dir
            rel_path = os.path.relpath(root, examples_dir)
            if rel_path == '.':
                rel_path = ''
                
            # Create the same structure in target dir
            for directory in dirs:
                dir_path = os.path.join(target_dir, rel_path, directory)
                os.makedirs(dir_path, exist_ok=True)
            
            # Copy each file
            for file in files:
                src_file = os.path.join(root, file)
                # Extract the subdirectory name (like 'GEOMETRY', 'IMAGES', etc.)
                sub_dir = os.path.basename(root) if os.path.basename(root) in ['GEOMETRY', 'IMAGES', 'PARAMETERS'] else ''
                
                if sub_dir:
                    # Ensure the subdirectory exists in target
                    os.makedirs(os.path.join(target_dir, sub_dir), exist_ok=True)
                    dst_file = os.path.join(target_dir, sub_dir, file)
                else:
                    dst_file = os.path.join(target_dir, file)
                    
                shutil.copy2(src_file, dst_file)
                print(f"Copied {src_file} to {dst_file}")
                
        print(f"Example files copied successfully to {target_dir}")
    
    except Exception as e:
        print(f"Error copying example files: {e}")
        raise
