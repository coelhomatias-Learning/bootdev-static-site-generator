import shutil
from pathlib import Path


def rcopydir(source: str | Path, dest: str | Path) -> None:
    source_path = Path(source)
    dest_path = Path(dest)

    if not source_path.exists():
        raise Exception(f"The source path {source_path} does not exist")

    if source_path.is_dir():
        if dest_path.exists():
            if not dest_path.is_dir():
                raise Exception(f"The destination path {dest_path} is not a directory")

            shutil.rmtree(dest_path)
        dest_path.mkdir()

        sources = source_path.glob("*")
        for src in sources:
            rcopydir(src, dest_path / src.name)

    elif source_path.is_file():
        shutil.copy(source_path, dest_path)
    else:
        raise Exception(f"Source path {source_path} is neither a file nor a directory")
