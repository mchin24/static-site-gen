import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.LINK, 'http://example.com')
        node2 = TextNode("This is a text node", TextType.LINK, 'http://example.com')
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.IMAGE, 'http://example.com/test.png')
        node2 = TextNode("This is a text node", TextType.IMAGE, 'http://example.com/test.png')
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.IMAGE, None)
        node2 = TextNode("This is a text node", TextType.IMAGE, None)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.LINK, 'http://example.com')
        node2 = TextNode("This is text node", TextType.LINK, 'http://google.com')
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.IMAGE, 'http://example.com/test.png')
        node2 = TextNode("This is a text node", TextType.IMAGE, 'http://example.com/test.jpg')
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.LINK, None)
        node2 = TextNode("This is text node", TextType.LINK, 'http://google.com')
        self.assertNotEqual(node, node2)

    def test_text_to_html(self):
        node = TextNode("This is normal text", TextType.TEXT)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "This is normal text")
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is normal text")

        node = TextNode("This is bold text", TextType.BOLD)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>This is bold text</b>")
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>This is italic text</i>")
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

        node = TextNode("This is code text", TextType.CODE)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>This is code text</code>")
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code text")

        node = TextNode("This is link text", TextType.LINK, "http://example.com")
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="http://example.com">This is link text</a>')
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is link text")

        node = TextNode("This is image text", TextType.IMAGE, "http://example.com/test.png")
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<img src="http://example.com/test.png" alt="This is image text"></img>')
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")

if __name__ == "__main__":
    unittest.main()
    