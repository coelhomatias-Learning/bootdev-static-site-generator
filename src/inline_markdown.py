import re
from collections.abc import Callable
from typing import Literal

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    splits: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            splits.append(node)
            continue

        splited = node.text.split(delimiter)

        if not delimiter:
            raise Exception(f"Delimiter {delimiter} not valid")

        if len(splited) % 2 == 0:
            raise Exception("Invalid markdown, formated section not closed")

        for i, s in enumerate(splited):
            if not s:
                continue

            if i % 2 != 0:
                splits.append(TextNode(s, text_type))
            else:
                splits.append(TextNode(s, TextType.TEXT))

    return splits


PossibleObjects = Literal[TextType.IMAGE] | Literal[TextType.LINK]


def _split_text(
    text: str,
    object: tuple[str, str],
    object_type: PossibleObjects,
):
    text_objects = []
    match object_type:
        case TextType.IMAGE:
            delimiter = f"![{object[0]}]({object[1]})"
        case TextType.LINK:
            delimiter = f"[{object[0]}]({object[1]})"
        case _:
            raise Exception("Wrong object_type {object_type}")

    splited = text.split(delimiter, 1)

    if splited[0]:
        text_objects.append(TextNode(splited[0], TextType.TEXT))

    if len(splited) == 1:
        return text_objects

    text_objects.append(TextNode(object[0], object_type, object[1]))
    return text_objects, splited[1]


def split_nodes_func(
    old_nodes: list[TextNode], node_type: PossibleObjects, func: Callable
):
    splits: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            splits.append(node)
            continue

        objects = func(node.text)

        if not objects:
            splits.append(node)
            continue

        remaining_text = node.text
        for obj in objects:
            temp_splits, remaining_text = _split_text(remaining_text, obj, node_type)
            splits.extend(temp_splits)

        if remaining_text:
            splits.append(TextNode(remaining_text, TextType.TEXT))

    return splits


def split_nodes_image(old_nodes: list[TextNode]):
    return split_nodes_func(old_nodes, TextType.IMAGE, extract_mardown_images)


def split_nodes_link(old_nodes: list[TextNode]):
    return split_nodes_func(old_nodes, TextType.LINK, extract_mardown_links)


def extract_mardown_images(text: str):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_mardown_links(text: str):
    return re.findall(r" \[(.*?)\]\((.*?)\)", text)


def text_to_textnodes(text: str):
    node = TextNode(text, TextType.TEXT)
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([node], "**", TextType.BOLD),
                    "*",
                    TextType.ITALIC,
                ),
                "`",
                TextType.CODE,
            )
        )
    )
