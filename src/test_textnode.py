import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, normal, https://www.boot.dev)", repr(node)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_converstion(self):
        node = TextNode("This is a test text node", TextType.TEXT)
        node2 = LeafNode(None, "This is a test text node")
        self.assertEqual(text_node_to_html_node(node).to_html(), node2.to_html())

    def test_image_converstion(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        node2 = LeafNode(
            "img", "", {"src": "https://www.boot.dev", "alt": "This is an image"}
        )
        self.assertEqual(text_node_to_html_node(node).to_html(), node2.to_html())

    def test_bold_converstion(self):
        node = TextNode("This is bold text", TextType.BOLD)
        node2 = LeafNode("b", "This is bold text")
        self.assertEqual(text_node_to_html_node(node).to_html(), node2.to_html())

    def test_code_converstion(self):
        node = TextNode("This is super optimized code, ah, not", TextType.CODE)
        node2 = LeafNode("code", "This is super optimized code, ah, not")
        self.assertEqual(text_node_to_html_node(node).to_html(), node2.to_html())

    def test_italic_convertion(self):
        node = TextNode("This is italian text", TextType.ITALIC)
        node2 = LeafNode("i", "This is italian text")
        self.assertEqual(text_node_to_html_node(node).to_html(), node2.to_html())

    def test_link_convertion(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        node2 = LeafNode("a", "This is a link", {"href": "https://www.boot.dev"})
        self.assertEqual(text_node_to_html_node(node).to_html(), node2.to_html())


if __name__ == "__main__":
    unittest.main()
