def markdown_to_blocks(markdown: str):
    splited = markdown.split("\n\n")
    result = [i.strip() for i in splited if i]
    return result
