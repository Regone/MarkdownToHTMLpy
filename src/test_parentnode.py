import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode([
        LeafNode("Bold text","b"),
        LeafNode("Normal text",None),
        LeafNode("italic text","i"),
        LeafNode("Normal text", None),
    ],"p")
        self.assertEqual(node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    def test_eq2(self):
        node = ParentNode([
        LeafNode("bombaaaaaai","a"),
        LeafNode("Normal text",None),
        LeafNode("paragraphhy text","p"),
        LeafNode("Normal text", None),
    ],"p")
        self.assertEqual(node.to_html(),"<p><a>bombaaaaaai</a>Normal text<p>paragraphhy text</p>Normal text</p>")
    def test_eq3(self):
        node = ParentNode([
        LeafNode("Bold text","b"),
        LeafNode("Bold text","b"),
        LeafNode("Bold text","b"),
        LeafNode("Normal text",None),
        LeafNode("italic text","i"),
        LeafNode("Normal text", None),
    ],"p")
        self.assertEqual(node.to_html(),"<p><b>Bold text</b><b>Bold text</b><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
            
        

if __name__ == "__main__":
    unittest.main()