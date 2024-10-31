from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, value, tag = None, props = None):
        super().__init__(tag,value,None,props)    
    def to_html(self):
        if(self.value == None):
            raise ValueError
        if(self.tag == None):
            return str(self.value)
        s = ""
        s+= f"<{self.tag}"
        if(not self.props == None):
            s+=self.props_to_html()
        s+=">"
        s+= str(self.value)
        s+= f"</{self.tag}>"
        return s