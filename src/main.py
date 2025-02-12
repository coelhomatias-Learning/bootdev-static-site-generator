from pathlib import Path

from project_io import rcopydir
from utils import generate_page


def main():
    static_path = Path("static")
    generated_path = Path("public")
    md_page_path = Path("content/index.md")
    template_path = Path("template.html")
    html_page_path = Path("public/index.html")

    rcopydir(static_path, generated_path)
    generate_page(md_page_path, template_path, html_page_path)


if __name__ == "__main__":
    main()
