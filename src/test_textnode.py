import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from utils import split_nodes_delimiter


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

    def test_converstion(self):
        node = TextNode("This is a test text node", TextType.NORMAL)
        node2 = LeafNode(None, "This is a test text node")
        self.assertEqual(text_node_to_html_node(node).to_html(), node2.to_html())

    # TODO: Write tests for the other TextTypes

    def test_splits_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        correct = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(correct, new_nodes)


if __name__ == "__main__":
    unittest.main()
