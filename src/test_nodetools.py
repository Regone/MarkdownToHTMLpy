import unittest

from leafnode import LeafNode
from nodetools import NodeTools
from textnode import *

class TestTextNode(unittest.TestCase):
    # def test_eq(self):
    #     node = TextNode("This is text with a `code block` word", TextType.TEXT)
    #     node2 = NodeTools.split_nodes_delimiter(node, "`", TextType.CODE)
    #     nodes = [
    #             TextNode("This is text with a ", TextType.TEXT),
    #             TextNode("code block", TextType.CODE),
    #             TextNode(" word", TextType.TEXT),
    #             ]
    #     self.assertEqual(node2, nodes)
    
    def test_eq2(self):
        node2= NodeTools.extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(node2, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])    
        
    def test_eq3(self):
        node2= NodeTools.extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(node2, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])    
        
    def test_split_nodes_image(self):
        # Test 1: No images
        node = TextNode("Hello world!", TextType.TEXT)
        
        # Test 2: One image in middle
        node2 = TextNode("Start ![image](https://url.com) end", TextType.TEXT)
        
        # Test 3: Multiple images
        node3 = TextNode(
            "![first](url1) middle ![second](url2) end",
            TextType.TEXT
        )

    def test_split_nodes_link(self):
        # Test 1: No links
        node = TextNode("Just plain text", TextType.TEXT)
        
        # Test 2: One link
        node2 = TextNode("Click [here](https://boot.dev) please", TextType.TEXT)
        
        # Test 3: Multiple links with text between
        node3 = TextNode(
            "Start [link1](url1) middle [link2](url2) end",
            TextType.TEXT
        )    
        
    def test_split_nodes_all(self):
        node = TextNode("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)
        node= NodeTools.text_to_textnodes(node.text)
        self.assertEqual(node,[
                                TextNode("This is ", TextType.TEXT),
                                TextNode("text", TextType.BOLD),
                                TextNode(" with an ", TextType.TEXT),
                                TextNode("italic", TextType.ITALIC),
                                TextNode(" word and a ", TextType.TEXT),
                                TextNode("code block", TextType.CODE),
                                TextNode(" and an ", TextType.TEXT),
                                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                TextNode(" and a ", TextType.TEXT),
                                TextNode("link", TextType.LINK, "https://boot.dev"),
                            ])
if __name__ == "__main__":
    unittest.main()