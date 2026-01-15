import unittest
from textnode import TextNode, TextType
from utils import split_nodes_delimiter

class TestSplitTextNodes(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        nodes = TextNode("This is a test. `Split this code`. This is after split. `And this code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([nodes], "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is a test. ")
        self.assertEqual(new_nodes[1].text, "Split this code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, ". This is after split. ")
        self.assertEqual(new_nodes[3].text, "And this code")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)

        nodes = TextNode("This is a test. _This should be italicized_. This is after split. _As should this._", TextType.TEXT)
        new_nodes = split_nodes_delimiter([nodes], "_", TextType.ITALIC)

        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is a test. ")
        self.assertEqual(new_nodes[1].text, "This should be italicized")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, ". This is after split. ")
        self.assertEqual(new_nodes[3].text, "As should this.")
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)

        nodes = TextNode("This is a test. **This should be bolded**. This is after split. **As should this.**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([nodes], "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is a test. ")
        self.assertEqual(new_nodes[1].text, "This should be bolded")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, ". This is after split. ")
        self.assertEqual(new_nodes[3].text, "As should this.")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)

        nodes = TextNode("This is a test. _This should be ignored_. This is after split. **This should be bolded.**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([nodes], "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is a test. _This should be ignored_. This is after split. ")
        self.assertEqual(new_nodes[1].text, "This should be bolded.")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

if __name__ == "__main__":
    unittest.main()