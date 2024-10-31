import unittest

from leafnode import LeafNode
from nodetools import NodeTools
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is text with a `code block` word", TextType.Normal)
        node2 = NodeTools.split_nodes_delimiter(node, "`", TextType.Code)
        nodes = [
    TextNode("This is text with a ", TextType.Normal),
    TextNode("code block", TextType.Code),
    TextNode(" word", TextType.Normal),
]
        self.assertEqual(node2, nodes)
    
        
if __name__ == "__main__":
    unittest.main()