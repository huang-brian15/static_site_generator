import os
import shutil

def copy_files_recursive(source_dir_path: str, dest_dir_path: str):
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


    ## The below deletes entire directories before copying.
    # if not os.path.exists(source_dir_path):
    #     raise ValueError(f"Source directory {source_dir_path} does not exist.")
    #
    # if not os.path.isfile(source_dir_path):
    #     if not os.path.exists(dest_dir_path):
    #         os.mkdir(dest_dir_path)
    #     else:
    #         shutil.rmtree(dest_dir_path)
    #         os.mkdir(dest_dir_path)
    
    #     for path in os.listdir(source_dir_path):
    #         copy_static(os.path.join(source_dir_path, path), os.path.join(dest_dir_path, path))
    # else:
    #     shutil.copy(source_dir_path, dest_dir_path)