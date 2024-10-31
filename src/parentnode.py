from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, children, tag = None, props = None):
        super().__init__(tag,None,children,props)  
          
    def to_html(self):
        if(self.tag == None):
            raise ValueError
        if(self.children == None):
            raise ValueError
        elif(len(self.children)==0):
            raise ValueError
        
        
        s = ""
        if(self.tag != None):
            s+=f"<{self.tag}>"
        for child in self.children:
            if(isinstance(child.to_html(),str)):
                s+=child.to_html()
        if(self.tag != None):
            s+=f"</{self.tag}>"
        return s