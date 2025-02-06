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

        if not delimiter:
            raise Exception(f"Delimiter {delimiter} not valid")

        if len(splited) == 1:
            raise Exception(f"Delimiter {delimiter} not found in the node text")

        if len(splited) % 2 == 0:
            raise Exception("Invalid markdown, formated section not closed")

        for i, s in enumerate(splited):
            if not s:
                continue

            if i % 2 != 0:
                splits.append(TextNode(s, text_type))
            else:
                splits.append(TextNode(s, TextType.NORMAL))

    return splits
