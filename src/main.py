from textnode import TextNode
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnodes
)

from copy_static import copy_files_recursive

def main():
    static_path = "./static"
    public_path = "./public"
    copy_files_recursive(static_path, public_path)

if __name__ == '__main__':
    main()