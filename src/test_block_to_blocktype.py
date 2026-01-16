import unittest
from block import block_to_block_type, BlockType
from utils import markdown_to_blocks

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)

    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.heading)

        block = "###### This is a level 6 heading"
        self.assertEqual(block_to_block_type(block), BlockType.heading)

    def test_code(self):
        block = "```\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.code)

    def test_quote(self):
        block = "> This is a quote.\n> It spans multiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.quote)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.unordered_list)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ordered_list)

if __name__ == '__main__':
    unittest.main()