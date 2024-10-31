from cgitb import text
from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
        Normal = 1,
        BOLD = 2,
        Italic =3,
        Code = 4,
        Link = 5,
        Image = 6
        
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
            case TextType.Normal:
                return LeafNode(self.text)
            case TextType.BOLD:
                return LeafNode(self.text,"b") 
            case TextType.Italic:
                return LeafNode(self.text,"i")
            case TextType.Code:
                return LeafNode(self.text,"code")
            case TextType.Link:
                return LeafNode(self.text,"a",{"href": f"{self.url}","target":"_blank"})
            case TextType.Image:
                return LeafNode("","img",{"src": f"{self.url}","alt":f"{self.text}"})
            
            case _:
                pass