import unittest

from htmlnode import HTMLNode
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
    
    def test_markdown_to_blocks(self):
        node = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        node= NodeTools.markdown_to_blocks(node)
        self.assertEqual(node,[
    "# This is a heading",
    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
    "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
])
    def test_heading(self):
        block = "# Heading 1"
        self.assertEqual(NodeTools.block_to_block_type(block), "heading")

    def test_code(self):
        block = "```\ncode line 1\ncode line 2\n```"
        self.assertEqual(NodeTools.block_to_block_type(block), "code")

    def test_quote(self):
        block = "> Quote line 1\n> Quote line 2"
        self.assertEqual(NodeTools.block_to_block_type(block), "quote")

    def test_unordered_list(self):
        block = "* Item A\n* Item B\n- Item C"
        self.assertEqual(NodeTools.block_to_block_type(block), "unordered_list")

    def test_ordered_list(self):
        block = "1. Item A\n2. Item B\n3. Item C"
        self.assertEqual(NodeTools.block_to_block_type(block), "ordered_list")

    def test_paragraph(self):
        block = "This is a regular paragraph."
        self.assertEqual(NodeTools.block_to_block_type(block), "paragraph")
            
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = NodeTools.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = NodeTools.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = NodeTools.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )
    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = NodeTools.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""
        node = NodeTools.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

if __name__ == "__main__":
    unittest.main()