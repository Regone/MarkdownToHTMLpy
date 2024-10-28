from cgitb import text
from enum import Enum

class TextNode:
    
    class TextType(Enum):
        Normal = 1,
        Bold = 2,
        Italic =3,
        Code = 4,
        Link = 5,
        Image = 6
    
    def __init__(self, text,text_type,url = None):
        self.text = text
        self.text_type = text_type.value
        self.url = url
    
    def __eq__(self, value):
        return self.text == value.text and self.text_type==value.text_type and self.url == value.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"