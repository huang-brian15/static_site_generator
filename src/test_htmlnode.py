import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode


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


def main():
    unittest.main()

if __name__ == "__main__":
    main()