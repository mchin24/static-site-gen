from textnode import TextNode, TextType
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