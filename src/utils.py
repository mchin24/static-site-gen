
from textnode import TextNode, TextType
from leafnode import LeafNode

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
