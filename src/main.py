from textnode import TextNode
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links
)

def main():
    text_node_obj = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(text_node_obj)

    text_node_obj = TextNode("This is text with a `code block` word", "text")
    new_node = split_nodes_delimiter([text_node_obj], "`", "code")

    text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) \
                and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
    
    res = extract_markdown_images(text)


if __name__ == '__main__':
    main()