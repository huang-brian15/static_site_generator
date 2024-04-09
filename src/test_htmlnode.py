import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props1(self):
        d = {"href": "https://www.google.com", "target": "_blank"}
        html_node = HTMLNode(None, None, None, d)
        truth = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(html_node.props_to_html(), truth)

    def test_props2(self):
        d = {"href": "https://www.google.com", "target": "_blank", "test_key": "test_value"}
        html_node = HTMLNode(None, None, None, d)
        truth = " href=\"https://www.google.com\" target=\"_blank\" test_key=\"test_value\""
        self.assertEqual(html_node.props_to_html(), truth)


def main():
    unittest.main()

if __name__ == "__main__":
    main()