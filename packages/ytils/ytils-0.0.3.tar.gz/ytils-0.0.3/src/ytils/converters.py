import base64
import io
import re
import sys
from typing import Tuple


def PIL_image_to_base64(img, format="PNG") -> bytes:
    img_buffer = io.BytesIO()
    img.save(img_buffer, format=format)
    return base64.b64encode(img_buffer.getvalue())


def bytes_into_unit(bytes: float, units=["B", "KB", "MB", "GB", "TB"], precision=1) -> str:
    """Converts bytes into human readable size"""
    for unit in units:
        if bytes < 1024.0:
            break
        bytes /= 1024.0
    return f"{bytes:.{precision}f} {unit}"


def seconds_to(sec: int, *, to="hours|minutes") -> Tuple[int, int, int]:
    """
    Returns hours, minutes, seconds
    """
    assert to == "hours" or to == "minutes", "to can be hours or minutes"

    result = []
    min, sec = divmod(sec, 60)
    if "hours" in to:
        hrs, min = divmod(min, 60)
        result.append(hrs)
    else:
        result.append(0)

    result.append(min)
    result.append(sec)

    return tuple(result)


def sanitize_file_name(file_name: str, replace_with="_") -> str:
    """Remove prohibited symbols from file name"""
    prohibited_symbols = r'[\\/:*?"<>|]'  # List of prohibited symbols
    sanitized_file_name = re.sub(prohibited_symbols, replace_with, file_name)

    return sanitized_file_name


def image_to_base64(path: str, compress: int = None, markdown=False) -> str:
    if "Image" not in sys.modules:
        from PIL import Image

    image = Image.open(path)
    width, height = image.size
    print("Size:", f"{width}x{height}")
    if compress:
        new_size = (width // compress, height // compress)
        image = image.resize(new_size)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    b64 = base64.b64encode(buffered.getvalue())
    if markdown:
        return f"![Name](data:image/png;base64,{b64.decode()})"
    else:
        return base64.decode()


if __name__ == "__main__":
    sec = 6432
    h, m, s = seconds_to(sec, "hours")  # (1, 47, 12)
    print(h, m, s)
    h, m, s = seconds_to(sec, "minutes")  # (0, 107, 12)
    print(h, m, s)
