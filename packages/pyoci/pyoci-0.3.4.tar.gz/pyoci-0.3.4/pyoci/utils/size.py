# Code from https://stackoverflow.com/a/1094933
def human_readable_size(size: float) -> str:
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if size < 1024.0:
            return f"{size:3.1f}{unit}B"
        size /= 1024.0

    return f"{size:.1f}Yi"
