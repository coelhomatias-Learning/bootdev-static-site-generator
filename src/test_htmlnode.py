import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(
            "a",
            "This is a test message",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        correct_str = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), correct_str)

    def test_eq_repr(self):
        node = HTMLNode(
            "a",
            "This is a test message",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        correct_str = "HTMLNode(tag=a, value=This is a test message, children_len=[], props=dict_items([('href', 'https://www.google.com'), ('target', '_blank')]))"
        self.assertEqual(node.__repr__(), correct_str)

    def test_dif_props(self):
        node = HTMLNode(
            "a",
            "This is a test message",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        node2 = HTMLNode(
            "h",
            "This is a test message",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertNotEqual(node, node2)


class TestLeafNode(unittest.TestCase):
    def test_without_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), expected)

    def test_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
