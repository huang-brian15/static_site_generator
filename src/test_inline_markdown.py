import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
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


    def test_extract_markdown_images1(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) \
                and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        truth = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), 
                 ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        self.assertListEqual(extract_markdown_images(text), truth)


    def test_extract_markdown_lines1(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        truth = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertListEqual(extract_markdown_links(text), truth)


    def test_split_nodes_image1(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"
        node = TextNode(text, text_type_text)
        truth = [
                    TextNode("This is text with an ", text_type_text),
                    TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and another ", text_type_text),
                    TextNode("second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
                ]
        

    def test_split_nodes_image2(self):
        text = "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"
        node = TextNode(text, text_type_text)
        truth = [
                    TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and another ", text_type_text),
                    TextNode("second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
                ]

        self.assertListEqual(split_nodes_image([node]), truth)
    

    def test_split_nodes_image3(self):
        text = "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and some more text"
        node = TextNode(text, text_type_text)
        truth = [
                    TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and some more text", text_type_text),
                ]
        
        self.assertListEqual(split_nodes_image([node]), truth)
    

    def test_split_nodes_image_invalid_syntax(self):
        text = "!image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and some more text"
        node = TextNode(text, text_type_text)
        self.assertRaises(Exception, split_nodes_image([node]))
    

    def test_split_nodes_link1(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        node = TextNode(text, text_type_text)
        truth = [
                    TextNode("This is text with a ", text_type_text),
                    TextNode("link", text_type_link, "https://www.example.com"),
                    TextNode(" and ", text_type_text),
                    TextNode("another", text_type_link, "https://www.example.com/another")
                ]
        
        self.assertListEqual(split_nodes_link([node]), truth)

    
    def test_split_nodes_link2(self):
        text = "[link](https://www.example.com) and [another](https://www.example.com/another) and more text"
        node = TextNode(text, text_type_text)
        truth = [
                    TextNode("link", text_type_link, "https://www.example.com"),
                    TextNode(" and ", text_type_text),
                    TextNode("another", text_type_link, "https://www.example.com/another"),
                    TextNode(" and more text", text_type_text)
                ]
        
        self.assertListEqual(split_nodes_link([node]), truth)
    

    def test_split_nodes_link_invalid_syntax(self):
        text = "link(https://www.example.com) and [another](https://www.example.com/another) and more text"
        node = TextNode(text, text_type_text)
        self.assertRaises(Exception, split_nodes_link([node]))


    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        truth = [
                    TextNode("This is ", text_type_text),
                    TextNode("text", text_type_bold),
                    TextNode(" with an ", text_type_text),
                    TextNode("italic", text_type_italic),
                    TextNode(" word and a ", text_type_text),
                    TextNode("code block", text_type_code),
                    TextNode(" and an ", text_type_text),
                    TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and a ", text_type_text),
                    TextNode("link", text_type_link, "https://boot.dev"),
                ]
        self.assertListEqual(text_to_textnodes(text), truth)


def main():
    unittest.main()


if __name__ == "__main__":
    main()