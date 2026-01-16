from enum import Enum
import re

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

def block_to_block_type(block):
    if block.startswith('#') and block.find('# ') < 7:
        return BlockType.heading
    elif block.startswith('```') and block.endswith('```'):
        return BlockType.code
    elif block.startswith('> '):
        return BlockType.quote
    elif re.match(r'^\s*-\s+', block):
        return BlockType.unordered_list
    elif re.match(r'^\s*\d+\.\s+', block):
        return BlockType.ordered_list
    else:
        return BlockType.paragraph
    