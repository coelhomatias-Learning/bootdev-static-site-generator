from pathlib import Path

from project_io import rcopydir


def main():
    static_path = Path("static")
    generated_path = Path("public")

    rcopydir(static_path, generated_path)


if __name__ == "__main__":
    main()
