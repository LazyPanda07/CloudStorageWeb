from pathlib import Path


def prev_folder(current_path: Path):
    if current_path == Path("Home"):
        return current_path
    else:
        return current_path.parent
