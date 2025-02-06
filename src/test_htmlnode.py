import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        correct_str = ' href="https://www.google.com" target="_blank"'
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

    def test_without_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)


class TestParentNode(unittest.TestCase):
    def test_with_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        correct_str = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(correct_str, node.to_html())

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
