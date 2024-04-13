import os
import shutil

def copy_files_recursive(source_dir_path: str, dest_dir_path: str):
    """
    This method copies all contents (including subdirectories) of a 
    source directory into a destination directory.
    """
    if not os.path.exists(source_dir_path):
        raise ValueError(f"Source directory {source_dir_path} does not exist.")

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    
    for path in os.listdir(source_dir_path):
        src = os.path.join(source_dir_path, path)
        dest = os.path.join(dest_dir_path, path)
        print(f" * {src} -> {dest}")
        if os.path.isfile(src):
            shutil.copy(src, dest)
        else:
            copy_files_recursive(src, dest)