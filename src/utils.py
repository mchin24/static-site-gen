from leafnode import LeafNode
from textnode import TextNode, TextType
from block import BlockType, block_to_block_type
from htmlnode import HTMLNode
from parentnode import ParentNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or not node.text_type == TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 != 1:
            raise ValueError("Invalid markdown syntax: unmatched delimiter")
        for i in range(len(parts)):
            part = parts[i]
            if i % 2 == 0:
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
        
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r'!\[([^\]]*)\]\(([^\)]*)\)', text)

def extract_markdown_links(text):
    return re.findall(r'\[([^\]]*)\]\(([^\)]*)\)', text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or not node.text_type == TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        for image in images:
            alt_text, url = image
            split_text = node.text.split(f"![{alt_text}]({url})", 1)
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            node.text = split_text[1]

        if node.text:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or not node.text_type == TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        for link in links:
            text, url = link
            split_text = node.text.split(f"[{text}]({url})", 1)
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            node.text = split_text[1]

        if node.text:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
    return new_nodes

def text_to_text_nodes(text):
    if len(text) == 0:
        return []
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_link(split_nodes_image(text_nodes))
    text_nodes = split_nodes_image(split_nodes_image(text_nodes))
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)

    return text_nodes

def markdown_to_blocks(markdown):
    if len(markdown) == 0:
        return []
    
    blocks = [item.strip() for item in markdown.split("\n\n") if item.strip()]
    for block in blocks:
        block = block.strip()

    return blocks

def markdown_to_html_node(markdown):
    if len(markdown) == 0:
        return []
    
    node = ParentNode('div', [])

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.HEADING:
                level = block.count('#', 0, block.find(' '))  # Count leading '#' characters
                text_nodes = text_to_text_nodes(block[block.find(' ')+1:].strip())
                heading_node = ParentNode(f'h{level}', [])
                for text_node in text_nodes:
                        heading_node.children.append(TextNode.text_node_to_html_node(text_node))
                node.children.append(heading_node)
            
            case BlockType.PARAGRAPH:
                text_nodes = text_to_text_nodes(block)
                para_node = ParentNode('p', [])
                for text_node in text_nodes:
                    text_node.text = text_node.text.replace('\n', ' ')
                    para_node.children.append(TextNode.text_node_to_html_node(text_node))
                node.children.append(para_node)
            
            case BlockType.CODE:
                block = block[3:-3]
                if block.startswith('\n'):
                    block = block.replace('\n', '', 1)
                code_node = ParentNode('pre', [LeafNode('code', block)])
                node.children.append(code_node)
            
            case BlockType.QUOTE:
                content = block.replace('> ', '',1).strip()
                content = content.replace('\n> ', '\n')
                node.children.append(LeafNode('blockquote', content))
            
            case BlockType.UNORDERED_LIST:
                items = block.split('\n- ')
                items = [item for item in items if item.strip()]
                ul_node = ParentNode('ul', [])
                for item in items:
                    ul_node.children.append(LeafNode('li', item.replace('- ', '', 1).strip()))
                node.children.append(ul_node)
            
            case BlockType.ORDERED_LIST:
                items = block.split('\n')
                items = [item for item in items if item.strip()]
                ol_node = ParentNode('ol', [])
                for item in items:
                    ol_node.children.append(LeafNode('li', item[item.find('. ')+2:].strip()))
                node.children.append(ol_node)
            
            case _:
                continue

    return node
                