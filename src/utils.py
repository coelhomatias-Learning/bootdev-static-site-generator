import re
from pathlib import Path

from block_markdown import markdown_to_html_node


def extract_title(markdown: str) -> str:
    pattern = r"#{1} (.*)"
    titles = re.findall(pattern, markdown)
    if len(titles) == 0:
        raise Exception("No title found")
    return titles[0].strip()


def generate_page(
    from_path: Path | str, template_path: Path | str, dest_path: Path | str
) -> None:
    from_path = Path(from_path)
    template_path = Path(template_path)
    dest_path = Path(dest_path)

    if not from_path.is_file():
        raise Exception(f"From path {from_path} is not a file")

    if not template_path.is_file():
        raise Exception(
            f"Template file {template_path} is not a file or does not exist"
        )

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_str = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    final_html = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_str
    )

    with open(dest_path, "w") as f:
        f.write(final_html)


def generate_pages_recursive(
    dir_path_content: str | Path, template_path: str | Path, dest_dir_path: str | Path
):
    dir_path_content = Path(dir_path_content)
    template_path = Path(template_path)
    dest_dir_path = Path(dest_dir_path)

    if not dir_path_content.is_dir():
        raise Exception(f"Content path {dir_path_content} does not exist")

    if not template_path.is_file():
        raise Exception(
            f"Template file {template_path} is not a file or does not exist"
        )

    content = list(dir_path_content.rglob("*.md"))

    if not content:
        raise Exception(f"No content found in {dir_path_content}")

    dest_dir_path.mkdir(parents=True, exist_ok=True)

    for md in content:
        generate_page(
            md,
            template_path,
            str(md)
            .replace(str(dir_path_content), str(dest_dir_path))
            .replace(".md", ".html"),
        )
