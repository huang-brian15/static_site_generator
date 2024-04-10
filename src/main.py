from textnode import TextNode
from inline_markdown import split_nodes_delimiter

def main():
    text_node_obj = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(text_node_obj)

    text_node_obj = TextNode("This is text with a `code block` word", "text")
    new_node = split_nodes_delimiter([text_node_obj], "`", "code")

if __name__ == '__main__':
    main()