import unittest

from utils import extract_title


class TestUtils(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"
        correct = "Hello"
        self.assertEqual(correct, extract_title(markdown))

    def test_extract_title_with_whitespace(self):
        markdown = """
        # This is the title

        ## This is a subtitle

        # This is another title
        """
        correct = "This is the title"
        self.assertEqual(correct, extract_title(markdown))
