import unittest
from utils import extract_markdown_links, extract_markdown_images

class TestExtractLinksImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "Here is an image: ![Alt text](http://example.com/image.png) and another one ![Another image](http://example.com/another-image.jpg)"
        images = extract_markdown_images(text)
        expected_images = [
            ('Alt text', 'http://example.com/image.png'),
            ('Another image', 'http://example.com/another-image.jpg'),
        ]
        self.assertEqual(images, expected_images)

    def test_extract_markdown_links(self):
        text = "Here is a link: [Example](http://example.com) and another one [Google](http://google.com)"
        links = extract_markdown_links(text)
        expected_links = [
            ('Example', 'http://example.com'),
            ('Google', 'http://google.com')
        ]
        self.assertEqual(links, expected_links)

    def test_no_images_or_links(self):
        text = "This text has no images or links."
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertEqual(images, [])
        self.assertEqual(links, [])

    def test_malformed_markdown(self):
        text = "This is a malformed image ![Alt text(http://example.com/image.png and a malformed link [Example](http://example.com"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertEqual(images, [])
        self.assertEqual(links, [])


if __name__ == "__main__":
    unittest.main()