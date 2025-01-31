import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(
            "a",
            "O Alex é gay com certeza",
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
            "O Alex é gay com certeza",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        correct_str = "HTMLNode(tag=a, value=O Alex é gay com certeza, children_len=[], props=dict_items([('href', 'https://www.google.com'), ('target', '_blank')]))"
        self.assertEqual(node.__repr__(), correct_str)

    def test_dif_props(self):
        node = HTMLNode(
            "a",
            "O Alex é gay com certeza",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        node2 = HTMLNode(
            "h",
            "O Alex é gay com certeza",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
