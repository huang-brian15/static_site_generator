import os
import shutil

from copy_static import copy_files_recursive
from gen_content import (generate_page,
                         generate_pages_recursive)

def main():
    static_path = "./static"
    public_path = "./public"

    # Remove everything in public directory including directory
    print("Deleting public directory...")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    print("\n")

    # Copy everything from static directory into public directory
    print("Copying static files to public directory...")
    copy_files_recursive(source_dir_path=static_path, 
                         dest_dir_path=public_path)
    print("\n")

    # Specify: 
    # 1) Markdown file path 
    # 2) Path to HTML template for the Markdown text
    # 3) Directory to store the full HTML text
    content_path = "./content"
    template_path = "./template.html"
    html_dest_dir = "./public"

    print(f"Generating pages from {content_path} directory using {template_path}")
    generate_pages_recursive(dir_path_content=content_path, 
                             template_path=template_path, 
                             dest_dir_path=html_dest_dir)
    

if __name__ == '__main__':
    main()