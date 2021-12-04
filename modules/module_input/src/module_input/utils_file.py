import hashlib
import os
import typing

from img_processing_common.logger import logger


def files_in_path(path: typing.Union[str, bytes, os.PathLike]) -> typing.Generator:
    if not os.path.isdir(path):
        logger.error("module_input files_in_path not existing path %s", path)
    for _, _, filenames in os.walk(path):
        for file in filenames:
            yield file


def get_digest(file_path: typing.Union[str, bytes, os.PathLike]):
    l_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        while True:
            # Reading is buffered, so we can read smaller chunks.
            chunk = file.read(l_hash.block_size)
            if not chunk:
                break
            l_hash.update(chunk)

    return l_hash.hexdigest()
