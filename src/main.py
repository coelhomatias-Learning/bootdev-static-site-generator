from pathlib import Path

from project_io import rcopydir
from utils import generate_pages_recursive


def main():
    static_path = Path("static")
    generated_path = Path("public")
    content_dir_path = Path("content")
    template_path = Path("template.html")
    dest_dir_path = Path("public")

    rcopydir(static_path, generated_path)
    generate_pages_recursive(content_dir_path, template_path, dest_dir_path)


if __name__ == "__main__":
    main()
