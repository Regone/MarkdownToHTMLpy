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
    
    def test_eq2(self):
        node2= NodeTools.extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(node2, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])    
        
    def test_eq3(self):
        node2= NodeTools.extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(node2, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])    
        
if __name__ == "__main__":
    unittest.main()