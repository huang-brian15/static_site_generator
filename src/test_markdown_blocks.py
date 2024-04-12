import unittest
from markdown_blocks import (
    markdown_to_blocks,
    text_to_text_nodes_to_leaf_nodes,
    paragraph_to_html_node,
    heading_to_html_node,
    code_to_html_node,
    quote_to_html_node,
    unordered_list_to_html_node,
    ordered_list_to_html_node,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list
)

from htmlnode import (
    LeafNode,
    ParentNode)

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        
        blocks = markdown_to_blocks(text)
        truth = [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"
                ]
        self.assertEqual(blocks, truth)


    def test_markdown_to_blocks_leading_trailing_nl(self):
        text = """


This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items


"""
        
        blocks = markdown_to_blocks(text)
        truth = [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"
                ]
        self.assertEqual(blocks, truth)


    def test_markdown_to_blocks_trailing_nl(self):
        text = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items

"""
        
        blocks = markdown_to_blocks(text)
        truth = [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"
                ]
        self.assertEqual(blocks, truth)


    def test_markdown_to_blocks_multi_nl(self):
        text = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(text)
        truth = [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"
                ]
        self.assertEqual(blocks, truth)

    def test_markdown_to_blocks_combined(self):
        text = """



This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items





"""
        blocks = markdown_to_blocks(text)
        truth = [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"
                ]
        self.assertEqual(blocks, truth)


    def test_block_to_block_type_paragraph(self):
        blocks = ["This is **bolded** paragraph",
                 "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line"
                 "#This is also a paragraph",
                 "``This is not code``",
                 "`This is also not code`",
                 "```This is not code as well``",
                 ">This may look like a quote\nBut it is not a quote",
                 "1This is not\n-an unordered list",
                 "*2This is not\nan unordered list",
                 "- 3This is not\nan unordered list",
                 "* 4This is not \nan unordered list",
                 "1 This is not an ordered list",
                 "1. This is also not an \n2 ordered list ",
                 "1. This is also not \n2. an ordered list\n3 with a fake third item"
                 ]
        
        for block in blocks:
            self.assertEqual(block_to_block_type(block), block_type_paragraph)


    def test_block_to_block_type_heading(self):
        blocks = ["# This is heading1",
                  "## This is heading2",
                  "### This is heading3",
                  "#### This is heading4",
                  "##### This is heading5",
                  "###### This is heading6",
                  ]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), block_type_heading)


    def test_block_to_block_type_code(self):
        blocks = ["```This is code```",
                  "```     This is also code     \n```",
                  "```\n This too is also code \n```"
                  ]
        
        for block in blocks:
            self.assertEqual(block_to_block_type(block), block_type_code)


    def test_block_to_block_type_quote(self):
        blocks = [">This is a quote",
                  "> This is also a quote",
                  ">This is a quote\n>This is also part of the quote",
                  "> This is the second quote\n> This is also part of the second quote"
                  ]
        
        for block in blocks:
            self.assertEqual(block_to_block_type(block), block_type_quote)


    def test_block_to_block_type_unordered_list(self):
        blocks = ["-1This is first item in unordered list\n-This is second item in unordered list",
                  "*2This is first item in unordered list\n*This is second item in unordered list",
                  "- 3This is first item in unordered list\n- This is second item in unordered list",
                  "* 4This is first item in unordered list\n* This is second item in unordered list"
                  ]
        
        for block in blocks:
            self.assertEqual(block_to_block_type(block), block_type_unordered_list)


    def test_block_to_block_type_ordered_list(self):
        blocks = ["1.This is the first ordered list ",
                  "1. This is the first ordered list with spacing ",
                  "1.This is the second\n2.ordered list ",
                  "1. This is the second\n2. ordered list with spacing  ",
                  "1.This is the third\n2.ordered list\n3.with a third item",
                  "1. This is the third\n2. ordered list\n3. with a third item with spacing"
                  ]
        
        for block in blocks:
            self.assertEqual(block_to_block_type(block), block_type_ordered_list)


    def test_block_to_block_types_other(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)
    

    def test_text_to_text_nodes_to_leaf_nodes(self):
        text = "This is just some **bolded text** with some *italic text* with ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and [link](https://www.example.com) and some ```code```"
        truth = [LeafNode(tag=None, value="This is just some "),
                 LeafNode(tag="b", value="bolded text"),
                 LeafNode(tag=None, value=" with some "),
                 LeafNode(tag="i", value="italic text"),
                 LeafNode(tag=None, value=" with "),
                 LeafNode(tag="img", value="", props={"src": "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png", "alt": "image"}),
                 LeafNode(tag=None, value=" and "),
                 LeafNode(tag="a", value="link", props={"href": "https://www.example.com"}),
                 LeafNode(tag=None, value=" and some "),
                 LeafNode(tag="code", value="code")
                 ]
        
        nodes = text_to_text_nodes_to_leaf_nodes(text)
        self.assertListEqual(nodes, truth)


    def test_paragraph_to_html_node(self):
        text = "This is another paragraph with *italic* text and `code` here.\nThis is the same paragraph on a new line with more *italic text*"
        truth_children = [LeafNode(tag=None, value="This is another paragraph with "),
                          LeafNode(tag="i", value="italic"),
                          LeafNode(tag=None, value=" text and "),
                          LeafNode(tag="code", value="code"),
                          LeafNode(tag=None, value=" here. This is the same paragraph on a new line with more "),
                          LeafNode(tag="i", value="italic text")
                          ]
        
        truth = ParentNode(tag="p", children=truth_children)
        self.assertEqual(paragraph_to_html_node(text), truth)

        text = " This is another paragraph with *italic* text and `code` here.\nThis is the same paragraph on a new line with more *italic text* "
        truth_children = [LeafNode(tag=None, value=" This is another paragraph with "),
                          LeafNode(tag="i", value="italic"),
                          LeafNode(tag=None, value=" text and "),
                          LeafNode(tag="code", value="code"),
                          LeafNode(tag=None, value=" here. This is the same paragraph on a new line with more "),
                          LeafNode(tag="i", value="italic text"),
                          LeafNode(tag=None, value=" ")
                          ]
        
        truth = ParentNode(tag="p", children=truth_children)
        self.assertEqual(paragraph_to_html_node(text), truth)


    def test_heading_to_html_node(self):
        text = "###### This is a **bold** heading1 with *italics*"
        truth_children = [LeafNode(tag=None, value="This is a "),
                          LeafNode(tag="b", value="bold"),
                          LeafNode(tag=None, value=" heading1 with "),
                          LeafNode(tag="i", value="italics")
                          ]
        
        truth = ParentNode(tag="h6", children=truth_children)
        self.assertEqual(heading_to_html_node(text), truth)

        text = "##### This is a **bold** heading1 with *italics*"
        truth_children = [LeafNode(tag=None, value="This is a "),
                          LeafNode(tag="b", value="bold"),
                          LeafNode(tag=None, value=" heading1 with "),
                          LeafNode(tag="i", value="italics")
                          ]
        
        truth = ParentNode(tag="h5", children=truth_children)
        self.assertEqual(heading_to_html_node(text), truth)

        text = "#### This is a **bold** heading1 with *italics*"
        truth_children = [LeafNode(tag=None, value="This is a "),
                          LeafNode(tag="b", value="bold"),
                          LeafNode(tag=None, value=" heading1 with "),
                          LeafNode(tag="i", value="italics")
                          ]
        
        truth = ParentNode(tag="h4", children=truth_children)
        self.assertEqual(heading_to_html_node(text), truth)

        text = "### This is a **bold** heading1 with *italics*"
        truth_children = [LeafNode(tag=None, value="This is a "),
                          LeafNode(tag="b", value="bold"),
                          LeafNode(tag=None, value=" heading1 with "),
                          LeafNode(tag="i", value="italics")
                          ]
        
        truth = ParentNode(tag="h3", children=truth_children)
        self.assertEqual(heading_to_html_node(text), truth)

        text = "## This is a **bold** heading1 with *italics*"
        truth_children = [LeafNode(tag=None, value="This is a "),
                          LeafNode(tag="b", value="bold"),
                          LeafNode(tag=None, value=" heading1 with "),
                          LeafNode(tag="i", value="italics")
                          ]
        
        truth = ParentNode(tag="h2", children=truth_children)
        self.assertEqual(heading_to_html_node(text), truth)

        text = "# This is a **bold** heading1 with *italics*"
        truth_children = [LeafNode(tag=None, value="This is a "),
                          LeafNode(tag="b", value="bold"),
                          LeafNode(tag=None, value=" heading1 with "),
                          LeafNode(tag="i", value="italics")
                          ]
        
        truth = ParentNode(tag="h1", children=truth_children)
        self.assertEqual(heading_to_html_node(text), truth)

        text = "####### This is a **bold** heading1 with *italics*"
        with self.assertRaises(ValueError):
            heading_to_html_node(text)


    def test_code_to_html_node(self):
        text = "``` **Code** that will be turned into *leaf* node ```"
        truth_children = [LeafNode(tag="b", value="Code"),
                          LeafNode(tag=None, value=" that will be turned into "),
                          LeafNode(tag="i", value="leaf"),
                          LeafNode(tag=None, value=" node")
                          ]
        
        code_node = ParentNode(tag="code", children=truth_children)
        truth = ParentNode(tag="pre", children=[code_node])
        self.assertEqual(code_to_html_node(text), truth)

        text = "```**Code** that will be turned into *leaf* node```"
        truth_children = [LeafNode(tag="b", value="Code"),
                          LeafNode(tag=None, value=" that will be turned into "),
                          LeafNode(tag="i", value="leaf"),
                          LeafNode(tag=None, value=" node")
                          ]
        
        code_node = ParentNode(tag="code", children=truth_children)
        truth = ParentNode(tag="pre", children=[code_node])
        self.assertEqual(code_to_html_node(text), truth)


    def test_quote_to_html_node(self):
        text = "> This *is* a quote.\n> This is **also** part of the quote"
        truth_children = [LeafNode(tag=None, value="This "),
                          LeafNode(tag="i", value="is"),
                          LeafNode(tag=None, value=" a quote. This is "),
                          LeafNode(tag="b", value="also"),
                          LeafNode(tag=None, value=" part of the quote")
                          ]
        truth = ParentNode(tag="blockquote", children=truth_children)
        self.assertEqual(quote_to_html_node(text), truth)

        text = ">    This *is* a quote.    \n>    This is **also** part of the quote   "
        truth_children = [LeafNode(tag=None, value="This "),
                          LeafNode(tag="i", value="is"),
                          LeafNode(tag=None, value=" a quote. This is "),
                          LeafNode(tag="b", value="also"),
                          LeafNode(tag=None, value=" part of the quote")
                          ]
        truth = ParentNode(tag="blockquote", children=truth_children)
        self.assertEqual(quote_to_html_node(text), truth)


    def test_unordered_list_to_html_node(self):
        text = "- This is first *item* in unordered list\n- This is **second** item in unordered list"
        item1 = [LeafNode(tag=None, value="This is first "),
                 LeafNode(tag="i", value="item"),
                 LeafNode(tag=None, value=" in unordered list")
                 ]
        
        item2 = [LeafNode(tag=None, value="This is "),
                 LeafNode(tag="b", value="second"),
                 LeafNode(tag=None, value=" item in unordered list")
                 ]
        
        parent1 = ParentNode(tag="li", children=item1)
        parent2 = ParentNode(tag="li", children=item2)
        truth = ParentNode(tag="ul", children=[parent1, parent2])
        self.assertEqual(unordered_list_to_html_node(text), truth)
        
        text = "* This is first *item* in unordered list\n* This is **second** item in unordered list"
        item1 = [LeafNode(tag=None, value="This is first "),
                 LeafNode(tag="i", value="item"),
                 LeafNode(tag=None, value=" in unordered list")
                 ]
        
        item2 = [LeafNode(tag=None, value="This is "),
                 LeafNode(tag="b", value="second"),
                 LeafNode(tag=None, value=" item in unordered list")
                 ]
        
        parent1 = ParentNode(tag="li", children=item1)
        parent2 = ParentNode(tag="li", children=item2)
        truth = ParentNode(tag="ul", children=[parent1, parent2])
        self.assertEqual(unordered_list_to_html_node(text), truth)

        text = "*    This is first *item* in unordered list   \n*    This is **second** item in unordered list    "
        item1 = [LeafNode(tag=None, value="This is first "),
                 LeafNode(tag="i", value="item"),
                 LeafNode(tag=None, value=" in unordered list")
                 ]
        
        item2 = [LeafNode(tag=None, value="This is "),
                 LeafNode(tag="b", value="second"),
                 LeafNode(tag=None, value=" item in unordered list")
                 ]
        
        parent1 = ParentNode(tag="li", children=item1)
        parent2 = ParentNode(tag="li", children=item2)
        truth = ParentNode(tag="ul", children=[parent1, parent2])
        self.assertEqual(unordered_list_to_html_node(text), truth)


    def test_ordered_list_to_html_node(self):
        text = "1. This is first *item* in ordered list\n2. This is **second** item in ordered list"
        item1 = [LeafNode(tag=None, value="This is first "),
                 LeafNode(tag="i", value="item"),
                 LeafNode(tag=None, value=" in ordered list")
                 ]
        
        item2 = [LeafNode(tag=None, value="This is "),
                 LeafNode(tag="b", value="second"),
                 LeafNode(tag=None, value=" item in ordered list")
                 ]
        
        parent1 = ParentNode(tag="li", children=item1)
        parent2 = ParentNode(tag="li", children=item2)
        truth = ParentNode(tag="ol", children=[parent1, parent2])
        self.assertEqual(ordered_list_to_html_node(text), truth)

        text = "1.    This is first *item* in ordered list   \n2.    This is **second** item in ordered list     "
        item1 = [LeafNode(tag=None, value="This is first "),
                 LeafNode(tag="i", value="item"),
                 LeafNode(tag=None, value=" in ordered list")
                 ]
        
        item2 = [LeafNode(tag=None, value="This is "),
                 LeafNode(tag="b", value="second"),
                 LeafNode(tag=None, value=" item in ordered list")
                 ]
        
        parent1 = ParentNode(tag="li", children=item1)
        parent2 = ParentNode(tag="li", children=item2)
        truth = ParentNode(tag="ol", children=[parent1, parent2])
        self.assertEqual(ordered_list_to_html_node(text), truth)

        text = "1. This is first *item* in ordered list\n3. This is **second** item in ordered list"
        with self.assertRaises(ValueError):
            ordered_list_to_html_node(text)

def main():
    unittest.main()


if __name__ == "__main__":
    main()