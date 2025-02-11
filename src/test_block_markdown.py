import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks


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
