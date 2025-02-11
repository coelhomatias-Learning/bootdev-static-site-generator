import re
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


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
    return block.startswith("```") and block.endswith("```")


def is_quote_block(block: str):
    splited = [i.strip() for i in block.split("\n") if i.strip()]
    return all(map(lambda x: x.startswith(">"), splited))


def is_unordered_list_block(block: str):
    splited = [i.strip() for i in block.split("\n") if i.strip()]
    return all(map(lambda x: x.startswith("- ") or x.startswith("* "), splited))


def is_ordered_list_block(block: str):
    splited = [i.strip() for i in block.split("\n") if i.strip()]
    result = []
    for i, s in enumerate(splited):
        result.append(s.startswith(f"{i + 1}. "))
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


def _heading_level(heading: str):
    match = r"^(#{1,6})"
    return len(re.findall(match, heading)[0])


def heading_block_to_node(block: str) -> ParentNode:
    level = _heading_level(block)
    text_nodes = text_to_textnodes(block[level + 1 :])
    leaf_nodes: list[HTMLNode] = list(map(text_node_to_html_node, text_nodes))
    return ParentNode(f"h{level}", leaf_nodes)


def code_block_to_node(block: str) -> ParentNode:
    splited = [i for i in block.split("```") if i]
    code = "".join(splited)
    return ParentNode("pre", [LeafNode("code", code)])


def quote_block_to_node(block: str) -> ParentNode:
    splited = [i for i in block.split("\n") if i]
    quote = " ".join(map(lambda x: x[1:].strip(), splited))
    text_nodes = text_to_textnodes(quote)
    leaf_nodes: list[HTMLNode] = list(map(text_node_to_html_node, text_nodes))
    return ParentNode("blockquote", leaf_nodes)


def list_item_block_to_node(text: str) -> ParentNode:
    text_nodes = text_to_textnodes(text)
    leaf_nodes: list[HTMLNode] = list(map(text_node_to_html_node, text_nodes))
    return ParentNode("li", leaf_nodes)


def unordered_list_block_to_node(block: str) -> ParentNode:
    items = [i[2:] for i in block.split("\n") if i]
    node_items: list[HTMLNode] = list(map(list_item_block_to_node, items))
    return ParentNode("ul", node_items)


def ordered_list_block_to_node(block: str) -> ParentNode:
    items = [i[3:] for i in block.split("\n") if i]
    node_items: list[HTMLNode] = list(map(list_item_block_to_node, items))
    return ParentNode("ol", node_items)


def paragraph_block_to_node(block: str) -> ParentNode:
    p = " ".join([i for i in block.split("\n") if i])
    text_nodes = text_to_textnodes(p)
    leaf_nodes: list[HTMLNode] = list(map(text_node_to_html_node, text_nodes))
    return ParentNode("p", leaf_nodes)


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []

    for b in blocks:
        b_type = block_to_block_type(b)

        match b_type:
            case BlockType.HEADING:
                children.append(heading_block_to_node(b))
            case BlockType.CODE:
                children.append(code_block_to_node(b))
            case BlockType.QUOTE:
                children.append(quote_block_to_node(b))
            case BlockType.UNORDERED_LIST:
                children.append(unordered_list_block_to_node(b))
            case BlockType.ORDERED_LIST:
                children.append(ordered_list_block_to_node(b))
            case BlockType.PARAGRAPH:
                children.append(paragraph_block_to_node(b))
    return ParentNode("div", children)
