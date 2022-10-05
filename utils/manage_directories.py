from pathlib import Path


def remove_directory(directory_name):
    """Delete folders recursively."""
    directory = Path(directory_name)
    for item in directory.iterdir():
        if item.is_dir():
            remove_directory(item)
        else:
            item.unlink()
    directory.rmdir()


def create_directory_with_subdirectories(directory_name):
    Path(directory_name).mkdir(parents=True, exist_ok=True)
