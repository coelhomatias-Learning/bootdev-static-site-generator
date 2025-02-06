from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    splits: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            splits.append(node)
            continue

        splited = node.text.split(delimiter)

        if len(splited) == 1:
            raise Exception("Delimiter not found in the node text")

        _splits = [
            TextNode(splited[0], TextType.NORMAL),
            TextNode(splited[1], text_type),
            TextNode(splited[2], TextType.NORMAL),
        ]

        splits.extend(_splits)

    return splits
