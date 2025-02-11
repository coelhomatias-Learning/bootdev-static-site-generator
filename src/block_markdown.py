import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str):
    splited = markdown.split("\n\n")
    result = [i.strip() for i in splited if i.strip()]
    return result


def is_heading_block(block: str):
    heading = r"^#{1,6} (.*)"
    return re.findall(heading, block)


def is_code_block(block: str):
    return block[:3] == "```" and block[-3:] == "```"


def is_quote_block(block: str):
    splited = [i.strip() for i in block.split("\n") if i.strip()]
    return all(map(lambda x: x[0] == ">", splited))


def is_unordered_list_block(block: str):
    splited = [i.strip() for i in block.split("\n") if i.strip()]
    return all(map(lambda x: x[:2] == "- " or x[:2] == "* ", splited))


def is_ordered_list_block(block: str):
    splited = [i.strip() for i in block.split("\n") if i.strip()]
    result = []
    for i, s in enumerate(splited):
        result.append(s[0] == str(i + 1) and s[1:3] == ". ")
    return all(result)


def block_to_block_type(block: str):
    if is_heading_block(block):
        return BlockType.HEADING
    elif is_code_block(block):
        return BlockType.CODE
    elif is_quote_block(block):
        return BlockType.QUOTE
    elif is_unordered_list_block(block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list_block(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
