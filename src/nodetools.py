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
        # First normalize all newlines
        splitted_text = markdown.replace('\r\n', '\n')
        
        # Split into blocks using double newlines
        splitted_text = splitted_text.split('\n\n')
        
        merged_text = []
        for block in splitted_text:
            # Add protection against empty lines
            if block.strip():  # only process non-empty blocks
                # Check if this is a list block, but only if the line isn't empty
                is_list = (block.strip().startswith('*') or 
                        any(line.strip() and line.strip()[0].isdigit() 
                            for line in block.split('\n')))
                
                if is_list:
                    # For lists, keep the newlines
                    cleaned_block = block.strip()
                else:
                    # For non-lists, replace newlines with spaces
                    cleaned_block = block.replace('\n', ' ').strip()
                    
                if cleaned_block:
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
                    print("Original block:", repr(block))
                    clean_text = block[1:].strip()
                    print("Clean text:", repr(clean_text))
                    print("Children:", NodeTools.text_to_children(clean_text))
                    children = NodeTools.text_to_children(clean_text)
                    print("Children:", children)
                    nodes.append(ParentNode("blockquote", children))
                case "unordered_list":
                    list_items = []
                    for item in block.split('\n'):
                        if item.strip().startswith('*'):
                            list_items.append(ParentNode("li", NodeTools.text_to_children(item.lstrip('*').strip())))
                    nodes.append(ParentNode("ul", list_items))
                case "ordered_list":
                    nodes.append(ParentNode("ol",[ParentNode(f"li",None,NodeTools.text_to_children(block.split(". ", 1)[1].strip()))]))
                case "paragraph":
                    nodes.append(ParentNode(f"p",NodeTools.text_to_children(block.strip())))
        div = ParentNode("div",nodes,None)
        return div
        
        
        
    def text_to_children(text):
        nodes = NodeTools.text_to_textnodes(text)
        print("Text nodes:", nodes) 
        leafnodes = []
        for node in nodes:
            leafnodes.append(node.text_node_to_html_node())
            
        return leafnodes
        