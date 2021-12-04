"""
Shared functions to validate input file
"""

import os
import typing

from PIL import Image, UnidentifiedImageError

from .logger import logger
from .messaging import remove_msg


def is_image(path: typing.Union[str, bytes, os.PathLike]) -> True:
    try:
        Image.open(path).convert("RGBA")
        return True
    except (UnidentifiedImageError, FileNotFoundError, OSError):
        return False


def is_valid_input_file(
    file_path: typing.Union[str, bytes, os.PathLike], host: str, port: int, queue: str
) -> bool:
    if not is_image(file_path):
        logger.error("file is not valid image, deleting  %s", file_path)
        try:
            os.remove(file_path)
            remove_msg(host, port, queue)
            return False
        except FileNotFoundError:
            pass
    return True
