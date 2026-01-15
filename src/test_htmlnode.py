import unittest

from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "greeting"})
        expected_repr = "HTMLNode(tag='div', value='Hello', children='[]', props='{'class': 'greeting'}')"
        self.assertEqual(repr(node), expected_repr)

        node = HTMLNode(tag="p", value="Hello")
        expected_repr = "HTMLNode(tag='p', value='Hello', children=None, props=None)"
        self.assertEqual(repr(node), expected_repr)

        child_node = HTMLNode(tag="span", value="World")
        node = HTMLNode(tag="p", children=[child_node])
        expected_repr = "HTMLNode(tag='p', value=None, children='[HTMLNode(tag='span', value='World', children=None, props=None)]', props=None)"
        self.assertEqual(repr(node), expected_repr)

    def test_props_to_html(self):
        node = HTMLNode(tag="div", props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), 'class="container" id="main"')

        node = HTMLNode(tag="span", props={})
        self.assertEqual(node.props_to_html(), "")

        node = HTMLNode(tag="p", props=None)
        self.assertEqual(node.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()