from pathlib import Path


def next_folder(folder_name: str, current_path: Path):
    return current_path.joinpath(folder_name)
