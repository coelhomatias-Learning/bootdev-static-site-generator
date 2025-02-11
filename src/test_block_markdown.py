import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        correct = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]

        result = markdown_to_blocks(text)
        self.assertEqual(correct, result)

    def test_markdown_to_blocks_newlines(self):
        text = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        correct = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        result = markdown_to_blocks(text)
        self.assertEqual(correct, result)

    def test_is_heading_block(self):
        heading1 = "# This is a level 1 heading"
        heading2 = "## This is a level 2 heading"
        heading3 = "### This is a level 3 heading"
        heading4 = "#### This is a level 4 heading"
        heading5 = "########## This is an invalid heading"
        heading6 = " ##### This is another invalid heading"

        self.assertEqual(BlockType.HEADING, block_to_block_type(heading1))
        self.assertEqual(BlockType.HEADING, block_to_block_type(heading2))
        self.assertEqual(BlockType.HEADING, block_to_block_type(heading3))
        self.assertEqual(BlockType.HEADING, block_to_block_type(heading4))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(heading5))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(heading6))

    def test_is_code_block(self):
        code1 = "``` This is a code block ```"
        code2 = """
        ```
        This is another code block, I hope
        ```
        """
        code3 = """
        ``
        This is another code block
        But this one is invalid
        ```
        """

        self.assertEqual(BlockType.CODE, block_to_block_type(code1))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(code2))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(code3))

    def test_is_quote_block(self):
        quote1 = """
        >This is a valid quote
        >Yes it is
        """
        quote2 = """
        > This is a valid quote
        > Yes it is
        """
        quote3 = """
        This is not a valid quote
        >Yes it is
        """

        self.assertEqual(BlockType.QUOTE, block_to_block_type(quote1))
        self.assertEqual(BlockType.QUOTE, block_to_block_type(quote2))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(quote3))

    def test_is_unordered_list_block(self):
        unordered1 = "* list item1\n* list item2"
        unordered2 = "- list item1\n- list item2"
        unordered3 = "* list item1\n- list item2"
        unordered4 = " This is an invalid list\n* Although it has a correct list item"

        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(unordered1))
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(unordered2))
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(unordered3))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(unordered4))

    def test_is_ordered_list_block(self):
        ordered1 = "1. list item1\n2. list item2"
        ordered2 = "2. list item1\n3. list item2"
        ordered3 = "a. list item1\nb. list item2"
        ordered4 = "1. This is an invalid list\n3. Although it has a correct list item"

        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(ordered1))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(ordered2))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(ordered3))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(ordered4))

    #     def test_markdown_to_html(self):
    #         markdown = """
    # # This is a heading
    #
    # ## This is a subheading
    #
    # This is a paragraph of text. It has some **bold** and *italic* words inside of it.
    #
    # * This is the first list item in a list block
    # * This is a list item
    # * This is another list item
    #
    # > This is a quote
    # > Still part of the quote
    #
    # 1. An ordered list just for show
    # 2. With maybe 3 items
    # 3. Yeah, 3 it is
    #
    # ```
    # text = "This is a code block with some text"
    # print(text)
    # ```
    # """
    #         correct = ParentNode(
    #             "div",
    #             [
    #                 ParentNode("h1", [LeafNode(None, "This is a heading")]),
    #                 ParentNode("h2", [LeafNode(None, "This is a supheading")]),
    #                 ParentNode("p", [LeafNode(None, "This is a heading")]),
    #                 ParentNode("ul", [LeafNode(None, "This is a heading")]),
    #                 ParentNode("blockquote", [LeafNode(None, "This is a heading")]),
    #                 ParentNode("ol", [LeafNode(None, "This is a heading")]),
    #                 ParentNode("pre", [LeafNode(None, "This is a heading")]),
    #             ],
    #         )

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
