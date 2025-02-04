class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""

        return " ".join(map(lambda x: f'{x[0]}="{x[1]}"', self.props.items()))

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children_len={len(self.children) if self.children else []}, props={self.props.items() if self.props else {}})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        props: dict | None = None,
    ):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")

        if not self.tag:
            return self.value

        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
