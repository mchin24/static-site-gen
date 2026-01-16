import unittest
from utils import markdown_to_blocks, extract_title
from utils import TextNode, TextType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_blocks(self):
        markdown = '''
This is a simple text.

# This is a heading

- This is a list item.
- List item 2
        '''
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks, [
            "This is a simple text.",
            "# This is a heading",
            "- This is a list item.\n- List item 2"
        ])

    def test_empty_markdown(self):
        markdown = ''
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 0)
        self.assertEqual(blocks, [])

    def test_only_newlines(self):
        markdown = '\n\n\n'
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 0)
        self.assertEqual(blocks, [])

    def test_single_line(self):
        markdown = 'This is a simple text.\n\n# This is a heading\n\n- This is a list item.\n- List item 2'
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks, [
            "This is a simple text.",
            "# This is a heading",
            "- This is a list item.\n- List item 2"
        ])

    def test_extract_title(self):
        markdown = '''
# My Document Title 

Some other stuff here
    '''
        title = extract_title(markdown)
        self.assertEqual(title, "My Document Title")

    def test_extract_title_no_title(self):
        markdown = '''
Some text without a title.
- List item
        '''
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertTrue("No title found in markdown" in str(context.exception))

    if __name__ == '__main__':
        unittest.main() 