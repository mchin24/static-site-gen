import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node = LeafNode("p", "Hello, world!", props={"class": "intro"})
        self.assertEqual(node.to_html(), '<p class="intro">Hello, world!</p>')

        node = LeafNode("p", "Hello, world!", props={"class": "intro", "id": "first"})
        self.assertEqual(node.to_html(), '<p class="intro" id="first">Hello, world!</p>')

    def test_leaf_to_html_image(self):
        node = LeafNode("img", "", props={"src":"image.png", "alt": "An image", "width": "100"})
        self.assertEqual(node.to_html(), '<img src="image.png" alt="An image" width="100"></img>')

    def test_repr(self):
        node = LeafNode("span", "Sample Text")
        expected_repr = "HTMLNode(tag='span', value='Sample Text', props=None)"
        self.assertEqual(repr(node), expected_repr)   

        node = LeafNode("span", "Sample Text", props={"style": "color:red;", "class": "highlight"})
        expected_repr = "HTMLNode(tag='span', value='Sample Text', props='{'style': 'color:red;', 'class': 'highlight'}')"
        self.assertEqual(repr(node), expected_repr)