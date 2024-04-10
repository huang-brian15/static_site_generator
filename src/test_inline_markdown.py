import unittest
from inline_markdown import (
    split_nodes_delimiter,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold1(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )
    
    def test_delim_bold2(self):
        node = TextNode("This is text with a **bolded** **word**", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" ", text_type_text),
                TextNode("word", text_type_bold),
            ],
            new_nodes,
        )
    
    def test_delim_bold3(self):
        node = TextNode("**This** is text with a **bolded** **word**", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This", text_type_bold),
                TextNode(" is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" ", text_type_text),
                TextNode("word", text_type_bold),
            ],
            new_nodes,
        )
    
    def test_delim_bold_multiword(self):
        node = TextNode("**This** is text with a **bolded word** and another **word**", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This", text_type_bold),
                TextNode(" is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and another ", text_type_text),
                TextNode("word", text_type_bold),
            ],
            new_nodes,
        )
    
    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )
    
    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )


def main():
    unittest.main()


if __name__ == "__main__":
    main()