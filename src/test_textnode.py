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

if __name__ == "__main__":
    unittest.main()
    