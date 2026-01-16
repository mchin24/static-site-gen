import unittest
from utils import markdown_to_html_node
from htmlnode import HTMLNode

class TestMarkdownToHTML(unittest.TestCase):
    def test_heading_conversion(self):
        markdown = "# Heading 1"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), '<div><h1>Heading 1</h1></div>')

        markdown = "### Heading 3"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), '<div><h3>Heading 3</h3></div>')

        markdown = "###### Heading 6"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), '<div><h6>Heading 6</h6></div>')
       
    def test_paragraph_conversion(self):
        markdown = "This is a paragraph."
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), '<div><p>This is a paragraph.</p></div>')
    
    def test_code_block_conversion(self):
        markdown = "```\nprint('Hello, World!')\n```"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), '<div><pre><code>print(\'Hello, World!\')\n</code></pre></div>')

    def test_quote_block_conversion(self):
        markdown = "> This is a quote."
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), '<div><blockquote>This is a quote.</blockquote></div>')

        markdown = "> This is a quote.\n> Spanning multiple lines."
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), '<div><blockquote>This is a quote.\nSpanning multiple lines.</blockquote></div>')

    def test_unordered_list_conversion(self):
        markdown = "- Item 1\n- Item 2"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), '<div><ul><li>Item 1</li><li>Item 2</li></ul></div>')

    def test_ordered_list_conversion(self):
        markdown = "1. First item\n2. Second item"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), '<div><ol><li>First item</li><li>Second item</li></ol></div>')

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here ![alt text](https://example.com/image.png)

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here <img src=\"https://example.com/image.png\" alt=\"alt text\"></img></p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        

if __name__ == '__main__':
    unittest.main()