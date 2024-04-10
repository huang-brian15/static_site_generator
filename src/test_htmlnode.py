import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_html_attr1(self):
        d = {"href": "https://www.google.com", "target": "_blank"}
        html_node = HTMLNode(tag=None, value=None, children=None, props=d)
        truth = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(html_node.props_to_html(), truth)

    def test_html_attr2(self):
        d = {"href": "https://www.google.com", "target": "_blank", "test_key": "test_value"}
        html_node = HTMLNode(tag=None, value=None, children=None, props=d)
        truth = " href=\"https://www.google.com\" target=\"_blank\" test_key=\"test_value\""
        self.assertEqual(html_node.props_to_html(), truth)

    def test_leaf_node_no_tag(self):
        leaf_node = LeafNode(tag=None, value="test_value")
        truth = f"test_value"
        self.assertEqual(leaf_node.to_html(), truth)
    
    def test_leaf_node_no_value(self):
        leaf_node = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            leaf_node.to_html()

    def test_leaf_node_full(self):
        d = {"href": "https://www.google.com", "target": "_blank"}
        leaf_node = LeafNode(tag="a", value="my value", props=d)
        truth = f"<a href=\"https://www.google.com\" target=\"_blank\">my value</a>"
        self.assertEqual(leaf_node.to_html(), truth)
    
    def test_parent_node_single_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        truth = "<div><span>child</span></div>"
        self.assertEqual(parent_node.to_html(), truth)
    
    def test_parent_node_many_children(self):
        parent_node = ParentNode(
                                    "p",
                                    [
                                        LeafNode("b", "Bold text"),
                                        LeafNode(None, "Normal text"),
                                        LeafNode("i", "italic text"),
                                        LeafNode(None, "Normal text"),
                                    ],
                                )
        
        truth = f"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(parent_node.to_html(), truth)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        truth = "<div><span><b>grandchild</b></span></div>"
        self.assertEqual(parent_node.to_html(), truth)

    
def main():
    unittest.main()

if __name__ == "__main__":
    main()