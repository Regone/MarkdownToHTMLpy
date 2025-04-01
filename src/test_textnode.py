import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_eq2(self):
        node = TextNode("wata", TextType.IMAGE)
        node2 = TextNode("wata", TextType.IMAGE)
        self.assertEqual(node, node2)


    def test_eq3(self):
        node = TextNode("ima url ", TextType.LINK,"org.org")
        node2 = TextNode("ima url ", TextType.LINK,"org")
        self.assertNotEqual(node, node2)
    
    
    def test_eq4(self):
        node = TextNode("Hasta la vista", TextType.BOLD).text_node_to_html_node()
        node2 = LeafNode("Hasta la vista", "b")
        self.assertNotEqual(node, node2)
    def test_eq5(self):
        node = TextNode("Hasta la vista", TextType.BOLD).text_node_to_html_node()
        node2 = LeafNode("Hasta la vista", "b")
        self.assertNotEqual(node, node2)
        
if __name__ == "__main__":
    unittest.main()