class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        s = ""
        if(self.props == None):
            return ""
        
        for key, val in self.props.items():
            if(not s==""):
                s+=" "
            s+= f"{key}=\"{val}\""
        return s
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"            