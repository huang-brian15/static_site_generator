from markdown_blocks import (markdown_to_html_node,
                             markdown_to_blocks)

import os

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    """
    This method recursively generates HTML files/pages for all Markdown files
    listed in dir_path_content as well as its subdirectories.
    """

    for path in os.listdir(dir_path_content):
        src = os.path.join(dir_path_content, path)
        dest = os.path.join(dest_dir_path, path)
        if os.path.isfile(src):
            generate_page(src, template_path, dest.replace(".md", ".html"))
        else:
            generate_pages_recursive(src, template_path, dest)


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:

    """
    This method takes a markdown file, from_path, and extracts the title and content
    from this file. An HTML template file, template_path, is used as a template for 
    the title and content. After replacing the HTML template title and content with 
    the title and content from the markdown file, it gets saved into a new HTML file,
    dest_path.
    """

    # Read markdown file into variable
    md_file = open(from_path, 'r')
    markdown_text = md_file.read()
    md_file.close()

    # Read template into variable
    template_file = open(template_path, "r")
    template_text = template_file.read()
    template_file.close()

    # Get title from markdown text
    html_title = extract_title(markdown_text)

    # Get HTML text from markdown text
    html_node = markdown_to_html_node(markdown_text)
    html_text = html_node.to_html()
    
    # Replace title and content in HTML template with extracted title and content
    html_text_new = template_text.replace("{{ Title }}", html_title)
    html_text_new = html_text_new.replace("{{ Content }}", html_text)

    # Create destination directory and sub-directories recursively if they don't exist
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write HTML to new file or overrite file if exists
    dest_file = open(dest_path, "w")
    dest_file.write(html_text_new)
    dest_file.close()


def extract_title(markdown: str) -> str:
    """
    This method extracts the h1 heading from a Markdown text
    """
    
    blocks = markdown_to_blocks(markdown)
    heading = blocks[0].strip()
    if not heading.startswith("# "):
        raise ValueError(f"Invalid h1 header: {heading}")
    return heading.lstrip("# ")