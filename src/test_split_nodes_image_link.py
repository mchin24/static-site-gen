import unittest
from textnode import TextNode, TextType
from utils import split_nodes_image, split_nodes_link

class TestSplitNodesImageLink(unittest.TestCase):
    def test_split_nodes_image(self):
        old_nodes = [
            TextNode("This is a test ![alt text](http://example.com/image.png) end.", TextType.TEXT),
            TextNode("No image here.", TextType.TEXT),
            TextNode("First image ![first alt](http://example.com/another_image.jpg) and second image ![second alt](http://example.com/second_image.jpg)", TextType.TEXT),
            TextNode("Bad image ![bad alt]http://example.com/bad_image.jpg) and good image ![good alt](http://example.com/good_image.jpg)", TextType.TEXT),
            TextNode("Bad image ![bad alt(http://example.com/bad_image.jpg) and good image ![good alt](http://example.com/good_image.jpg)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(len(new_nodes), 12)
        self.assertEqual(new_nodes[0], TextNode("This is a test ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("alt text", TextType.IMAGE, "http://example.com/image.png"))
        self.assertEqual(new_nodes[2], TextNode(" end.", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("No image here.", TextType.TEXT))
        self.assertEqual(new_nodes[4], TextNode("First image ", TextType.TEXT))
        self.assertEqual(new_nodes[5], TextNode("first alt", TextType.IMAGE, "http://example.com/another_image.jpg"))
        self.assertEqual(new_nodes[6], TextNode(" and second image ", TextType.TEXT))
        self.assertEqual(new_nodes[7], TextNode("second alt", TextType.IMAGE, "http://example.com/second_image.jpg"))
        self.assertEqual(new_nodes[8], TextNode("Bad image ![bad alt]http://example.com/bad_image.jpg) and good image ", TextType.TEXT))
        self.assertEqual(new_nodes[9], TextNode("good alt", TextType.IMAGE, "http://example.com/good_image.jpg"))
        self.assertEqual(new_nodes[10], TextNode("Bad image ", TextType.TEXT))
        self.assertEqual(new_nodes[11], TextNode("bad alt(http://example.com/bad_image.jpg) and good image ![good alt", TextType.IMAGE, "http://example.com/good_image.jpg"))
        

    def test_split_nodes_link(self):
        old_nodes = [
            TextNode("This is a link [link text](http://example.com) end.", TextType.TEXT),
            TextNode("No link here.", TextType.TEXT),
            TextNode("First link [first link](http://example.com/another) and second link [second link](http://example.com/second)", TextType.TEXT),
            TextNode("Bad link [bad link(http://example.com/bad) and good link [good link](http://example.com/good)", TextType.TEXT),
            TextNode("Bad link [bad link]http://example.com/bad) and good link [good link](http://example.com/good)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(len(new_nodes), 12)
        self.assertEqual(new_nodes[0], TextNode("This is a link ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("link text", TextType.LINK, "http://example.com"))
        self.assertEqual(new_nodes[2], TextNode(" end.", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("No link here.", TextType.TEXT))
        self.assertEqual(new_nodes[4], TextNode("First link ", TextType.TEXT))
        self.assertEqual(new_nodes[5], TextNode("first link", TextType.LINK, "http://example.com/another"))
        self.assertEqual(new_nodes[6], TextNode(" and second link ", TextType.TEXT))
        self.assertEqual(new_nodes[7], TextNode("second link", TextType.LINK, "http://example.com/second"))
        self.assertEqual(new_nodes[8], TextNode("Bad link ", TextType.TEXT))
        self.assertEqual(new_nodes[9], TextNode("bad link(http://example.com/bad) and good link [good link", TextType.LINK, "http://example.com/good"))
        self.assertEqual(new_nodes[10], TextNode("Bad link [bad link]http://example.com/bad) and good link ", TextType.TEXT))
        self.assertEqual(new_nodes[11], TextNode("good link", TextType.LINK, "http://example.com/good"))

if __name__ == '__main__':
    unittest.main()