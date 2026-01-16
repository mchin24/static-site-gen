from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith('#') and block.find('# ') < 7:
        return BlockType.HEADING
    elif block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    elif block.startswith('> '):
        return BlockType.QUOTE
    elif re.match(r'^\s*-\s+', block):
        return BlockType.UNORDERED_LIST
    elif re.match(r'^\s*\d+\.\s+', block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    