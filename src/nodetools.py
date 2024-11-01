import re
from textnode import TextNode, TextType


class NodeTools():
    def split_nodes_delimiter(old_nodes, delimiter, text_type):
        nodes = old_nodes.text.split(delimiter)
        newnodes= []
        for n in range(0,len(nodes)):
            newnodes.append(TextNode(nodes[n], TextType.Normal if (n%2==0) else text_type))
        return newnodes
    
    def extract_markdown_images(text):
        s = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return s
    
    def extract_markdown_links(text):
        s = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return s
