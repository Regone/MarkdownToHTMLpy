from os import link
import re
from textnode import TextNode, TextType


class NodeTools():
    def split_nodes_delimiter( old_nodes, delimiter, text_type):
        result = []
        for node in old_nodes:
            if node.text_type != TextType.TEXT:
                result.append(node)
                continue
            pieces = node.text.split(delimiter)
            for i in range(len(pieces)):
                if pieces[i] == "":
                   continue
                current_type = TextType.TEXT if i % 2 == 0 else text_type
                result.append(TextNode(pieces[i], current_type))
            
        return result
    
    
    def extract_markdown_images(text):
        
        s = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return s
    
    def extract_markdown_links(text):
        s = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return s
    
    def split_nodes_image(old_nodes):
        result = []
        for node in old_nodes:
            images = NodeTools.extract_markdown_images(node.text)
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
            links = NodeTools.extract_markdown_links(node.text)
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
    
    def text_to_textnodes(text):
        nodes = [TextNode(text, TextType.TEXT)]
        # Split for each markdown type in sequence
        nodes = NodeTools.split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = NodeTools.split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        nodes = NodeTools.split_nodes_delimiter(nodes, "`", TextType.CODE)
        # Split for images and links last
        nodes = NodeTools.split_nodes_image(nodes)
        nodes = NodeTools.split_nodes_link(nodes)
        return nodes
        
        
    