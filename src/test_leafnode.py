import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("obana","<p>",{"href": "https://www.google.com","target":"_blank"})
        self.assertEqual(node.props_to_html(),"href=\"https://www.google.com\" target=\"_blank\"")
    def test_eq2(self):
        node = LeafNode("obana","<p>",{"href": "https://www.google.com","target":"_blank"})
        self.assertEqual(node.props_to_html(),"href=\"https://www.google.com\" target=\"_blank\"")
    def test_eq3(self):
        node = LeafNode("obana","<p>",{"href": "https://www.google.com","target":"_blank"})
        self.assertEqual(node.props_to_html(),"href=\"https://www.google.com\" target=\"_blank\"")
            
        

if __name__ == "__main__":
    unittest.main()