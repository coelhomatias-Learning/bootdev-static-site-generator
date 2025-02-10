import unittest

from textnode import TextNode, TextType
from utils import (
    extract_mardown_images,
    extract_mardown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.NORMAL
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.NORMAL),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.NORMAL
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_delim_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        correct = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        result = split_nodes_link([node])
        self.assertEqual(correct, result)

    def test_delim_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and again [to boot dev](https://www.boot.dev).",
            TextType.NORMAL,
        )
        correct = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(" and again ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(".", TextType.NORMAL),
        ]
        result = split_nodes_link([node])
        self.assertEqual(correct, result)

    def test_delim_image(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        correct = [
            TextNode("This is text with an image ", TextType.NORMAL),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        result = split_nodes_image([node])
        self.assertEqual(correct, result)

    def test_delim_images(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) and again ![to boot dev](https://www.boot.dev).",
            TextType.NORMAL,
        )
        correct = [
            TextNode("This is text with an image ", TextType.NORMAL),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(" and again ", TextType.NORMAL),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(".", TextType.NORMAL),
        ]
        result = split_nodes_image([node])
        self.assertEqual(correct, result)

    def test_delim_images_and_links(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and again ![to boot dev](https://www.boot.dev).",
            TextType.NORMAL,
        )
        correct = [
            TextNode("This is text with an image ", TextType.NORMAL),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(" and again ", TextType.NORMAL),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(".", TextType.NORMAL),
        ]
        result = split_nodes_link(split_nodes_image([node]))
        self.assertEqual(correct, result)


class TestRegex(unittest.TestCase):
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        correct = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        result = extract_mardown_images(text)

        self.assertEqual(correct, result)

    def test_extract_images_with_links(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        correct = [
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        result = extract_mardown_images(text)

        self.assertEqual(correct, result)

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        correct = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        result = extract_mardown_links(text)

        self.assertEqual(correct, result)

    def test_extract_links_with_images(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and an image ![to youtube](https://www.youtube.com/@bootdotdev)"
        correct = [("to boot dev", "https://www.boot.dev")]
        result = extract_mardown_links(text)

        self.assertEqual(correct, result)


if __name__ == "__main__":
    unittest.main()
