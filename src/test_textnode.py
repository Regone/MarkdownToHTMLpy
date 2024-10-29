import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_eq2(self):
        node = TextNode("wata", TextType.Image)
        node2 = TextNode("wata", TextType.Image)
        self.assertEqual(node, node2)

    def test_eq3(self):
        node = TextNode("ima url ", TextType.Link,"org.org")
        node2 = TextNode("ima url ", TextType.Link,"org")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()