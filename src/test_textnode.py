import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_uneq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is another text node", "bold")
        self.assertNotEqual(node, node2)

        node3 = TextNode("This is a text node", "bold")
        node4 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node3, node4)

    def test_empty_url(self):
        node = TextNode("TextNode", "bold")
        self.assertIsNone(node.url)
        

def main():
    unittest.main()

if __name__ == "__main__":
    main()