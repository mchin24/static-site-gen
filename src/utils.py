from leafnode import LeafNode
from textnode import TextNode, TextType
from block import BlockType, block_to_block_type
from htmlnode import HTMLNode
from parentnode import ParentNode
import re
import os
import shutil

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
    node = ParentNode('div', [])

    if len(markdown) == 0:
        return node

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
                    text_nodes = text_to_text_nodes(item.replace('- ', '', 1).strip())
                    li_children = []
                    for text_node in text_nodes:
                        li_children.append(TextNode.text_node_to_html_node(text_node))
                    li_node = ParentNode('li', li_children)
                    ul_node.children.append(li_node)
                node.children.append(ul_node)
            
            case BlockType.ORDERED_LIST:
                items = block.split('\n')
                items = [item for item in items if item.strip()]
                ol_node = ParentNode('ol', [])
                for item in items:
                    text_nodes = text_to_text_nodes(item[item.find('. ')+2:].strip())
                    li_children = []
                    for text_node in text_nodes:
                        li_children.append(TextNode.text_node_to_html_node(text_node))
                    li_node = ParentNode('li', li_children)
                    ol_node.children.append(li_node)
                node.children.append(ol_node)
            
            case _:
                continue

    return node

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith('# '):
            return block[2:].strip()
    raise Exception("No title found in markdown")
                
def copy_static_files(src_dir, dest_dir):
    # clear destination directory
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    # create the folder if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # copy source directory files
    files = os.listdir(src_dir)
    for file in files:
        file_path = os.path.join(src_dir, file)
        dest_path = os.path.join(dest_dir, file)
        if(os.path.isdir(file_path)):
            copy_static_files(file_path, dest_path)
        elif os.path.isfile(file_path):
            print(f"Copying {file} to {dest_dir}")
            shutil.copy(file_path, dest_path)
        
def generate_page(from_path, template_path, dest_path, basepath='/'):
    if not os.path.exists(os.path.abspath(from_path)):
        raise FileNotFoundError(f"Source file {from_path} does not exist.")
    
    if not os.path.exists(os.path.abspath(dest_path)):
        os.makedirs(os.path.abspath(dest_path))

    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")

    files = os.listdir(from_path)
    for file in files:
        if file.lower() == "index.md":
            src_file = open(os.path.abspath(os.path.join(from_path, file)), 'r').read()
            template_file = open(os.path.abspath(template_path), 'r').read()
            md_as_html = markdown_to_html_node(src_file).to_html()
            title = extract_title(src_file)

            template_file = template_file.replace("{{ Title }}", title)
            template_file = template_file.replace("{{ Content }}", md_as_html)
            
            template_file = template_file.replace('href="/', f'href="{basepath}')
            template_file = template_file.replace('src="/', f'src="{basepath}')

            dest_path = os.path.join(dest_path, "index.html")
            dest_file = open(os.path.abspath(dest_path), 'w')
            dest_file.write(template_file)
            dest_file.close()

        if os.path.isdir(os.path.join(from_path, file)):
            generate_page(os.path.abspath(os.path.join(from_path, file)), os.path.abspath(template_path), os.path.abspath(os.path.join(dest_path, file)))

