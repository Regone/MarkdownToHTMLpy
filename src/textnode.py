from cgitb import text
from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
        TEXT = 1,
        BOLD = 2,
        ITALIC =3,
        CODE = 4,
        LINK = 5,
        IMAGE = 6
        
class TextNode:
    
    
    
    def __init__(self, text,text_type,url = None):
        self.text = text
        self.text_type = text_type.value
        self.url = url
    
    def __eq__(self, value):
        return self.text == value.text and self.text_type==value.text_type and self.url == value.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def text_node_to_html_node(self):
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(self.text)
            case TextType.BOLD:
                return LeafNode(self.text,"b") 
            case TextType.ITALIC:
                return LeafNode(self.text,"i")
            case TextType.CODE:
                return LeafNode(self.text,"code")
            case TextType.LINK:
                return LeafNode(self.text,"a",{"href": f"{self.url}","target":"_blank"})
            case TextType.IMAGE:
                return LeafNode("","img",{"src": f"{self.url}","alt":f"{self.text}"})
            
            case _:
                pass