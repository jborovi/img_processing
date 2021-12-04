"""
main logic of module
checks input file
moves file to DATA_PROCESS folder
sends it to processing on OUTPUT_Q
"""

import asyncio
import json
import os
import typing
import uuid

import redis
from img_processing_common.logger import logger
from img_processing_common.messaging import send_message
from PIL import Image, UnidentifiedImageError

from .utils_file import files_in_path, get_digest

DATA_SOURCE = os.path.join(
    os.getenv("SHARED_VOLUME", "/tmp/images"),
    os.getenv("DIR_INPUT", "input"),
)
DATA_PROCESS = os.path.join(
    os.getenv("SHARED_VOLUME", "/tmp/images"),
    os.getenv("DIR_PROCESS", "process"),
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
OUTPUT_Q = os.getenv("INPUT_Q_MODULE_RGBA", "module_rgba")


def setup() -> None:
    if not os.path.exists(DATA_SOURCE):
        os.makedirs(DATA_SOURCE)
    if not os.path.exists(DATA_PROCESS):
        os.makedirs(DATA_PROCESS)


def process_inputs(path: typing.Union[str, bytes, os.PathLike]) -> None:
    for file_id in files_in_path(os.path.join(path)):
        try:
            sha_256 = get_digest(os.path.join(path, file_id))
            Image.open(os.path.join(path, file_id)).convert("RGBA")
        except FileNotFoundError:
            logger.error("received file which does not exist %s", file_id)
            continue
        except (UnidentifiedImageError, OSError) as exception:
            os.remove(os.path.join(path, file_id))
            logger.error("received malformed file %s", path)
            logger.error(str(exception))
            continue

        logger.info("received file sha256 hash %s", sha_256)
        session_id = str(uuid.uuid4())
        os.replace(
            os.path.join(DATA_SOURCE, file_id),
            os.path.join(DATA_PROCESS, f"{sha_256}_{session_id}"),
        )
        msg = json.dumps({"file_id": sha_256, "session_id": session_id}).encode()
        try:
            send_message(
                REDIS_HOST,
                REDIS_PORT,
                OUTPUT_Q,
                msg,
            )
        except redis.exceptions.ConnectionError:
            os.replace(
                os.path.join(DATA_PROCESS, f"{sha_256}_{session_id}"),
                os.path.join(DATA_SOURCE, sha_256),
            )


async def run() -> None:  # pragma: no cover
    setup()
    while True:
        process_inputs(DATA_SOURCE)
        await asyncio.sleep(0.1)
