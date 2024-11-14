from os import link
import re

from more_itertools import lstrip
from htmlnode import HTMLNode
from parentnode import ParentNode
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
        
    def markdown_to_blocks(markdown):
        splitted_text = markdown.replace('\r\n', '\n')
        splitted_text = splitted_text.split('\n\n')
        merged_text = []
        for block in splitted_text:
            cleaned_block = block.strip()
            if not cleaned_block:
                continue
            else:
                merged_text.append(cleaned_block)
        return merged_text    
    
    def block_to_block_type(block):
        lines = block.split('\n')

        if(re.match(r'#{1,6} ', block)):
            return "heading"
        elif block.startswith("```") and block.endswith("```"):
            return "code"
        elif all(line.startswith('>') for line in lines):
            return "quote"
        elif all(line.startswith('* ') or line.startswith('- ') for line in lines):
            return "unordered_list"
        elif all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
            return "ordered_list"
        return "paragraph"
    
    def markdown_to_html_node(markdown):
        blocks = NodeTools.markdown_to_blocks(markdown)
        nodes = []
        for block in blocks:
            match(NodeTools.block_to_block_type(block)):
                case "heading":
                    nodes.append(ParentNode(f"h{len(block)-len(block.lstrip('#'))}",NodeTools.text_to_children(block.lstrip('#').strip())))
                case "code":
                    nodes.append(ParentNode("pre",[ParentNode(f"code",None,NodeTools.text_to_children(block.strip("```").strip()))]))
                case "quote":
                    nodes.append(ParentNode(f"blockquote",NodeTools.text_to_children(block.lstrip('>').strip())))
                case "unordered_list":
                    nodes.append(ParentNode("ul",[ParentNode(f"li",None,NodeTools.text_to_children(block.lstrip('*').strip()))]))
                case "ordered_list":
                    nodes.append(ParentNode("ol",[ParentNode(f"li",None,NodeTools.text_to_children(block.split(". ", 1)[1].strip()))]))
                case "paragraph":
                    nodes.append(ParentNode(f"p",NodeTools.text_to_children(block.strip())))
        div = ParentNode(nodes,"div",None)
        return div
        
        
    def text_to_children(text):
        nodes = NodeTools.text_to_textnodes(text)
        leafnodes = []
        for node in nodes:
            leafnodes.append(node.text_node_to_html_node())
            
        return leafnodes
        