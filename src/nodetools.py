from os import link
import re
from textnode import TextNode, TextType


class NodeTools():
    def split_nodes_delimiter(old_nodes, delimiter, text_type):
        nodes = old_nodes.text.split(delimiter)
        newnodes= []
        for n in range(0,len(nodes)):
            newnodes.append(TextNode(nodes[n], TextType.TEXT if (n%2==0) else text_type))
        return newnodes
    
    def extract_markdown_images(text):
        s = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return s
    
    def extract_markdown_links(text):
        s = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return s
    
    def split_nodes_image(old_nodes):
        result = []
        for node in old_nodes:
            images = extract_markdown_images(node.text)
            if not images:
                result.append(node)
                continue
                
            current_text = node.text
            
            for img_alt, img_url in images:
                parts = current_text.split(f"![{img_alt}]({img_url})", 1)
                
                if parts[0]:
                    result.append(TextNode(parts[0], TextType.TEXT))
                    
                result.append(TextNode(img_alt, TextType.IMAGE, img_url))
                
                current_text = parts[1]
                
            if current_text:
                result.append(TextNode(current_text, TextType.TEXT))
        return result     
        
    def split_nodes_link(old_nodes):
        result = []
        for node in old_nodes:
            links = extract_markdown_links(node.text)
            if not links:
                result.append(node)
                continue
                
            current_text = node.text
            
            for link_txt, link_url in links:
                parts = current_text.split(f"[{link_txt}]({link_url})", 1)
                
                if parts[0]:
                    result.append(TextNode(parts[0], TextType.TEXT))
                    
                result.append(TextNode(link_txt, TextType.LINK, link_url))
                
                current_text = parts[1]
                
            if current_text:
                result.append(TextNode(current_text, TextType.TEXT))
        return result