"""
main logic of module
reads messages from INPUT_Q about rgba value of file and stores it in color folder
messages are read from FAILOVER_Q once
if received file is not valid picture, it gets deleted
"""

import asyncio
import json
import os
import typing

from img_processing_common.conf import DATA_DONE, DATA_PROCESS
from img_processing_common.logger import logger
from img_processing_common.messaging import (read_messages,
                                             read_messages_failover,
                                             remove_msg)
from img_processing_common.utils_img import is_valid_input_file

from .utils_color import get_colour_name
from .utils_file import create_path_color

INPUT_Q = os.getenv("INPUT_Q", "module_color")
FAILOVER_Q = f"processing_color_{os.getenv('WORKER_ID', 'unknown')}"

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


def get_message_data(msg: str) -> tuple:
    data = json.loads(msg.decode())
    return (
        data.get("rgba"),
        data.get("file_id"),
        data.get("session_id"),
    )


def move_file_to_color(
    file_path: typing.Union[str, bytes, os.PathLike], color: str, file_id: str
) -> bool:
    try:
        os.replace(
            file_path,
            os.path.join(
                create_path_color(color),
                file_id,
            ),
        )
        logger.info("moved %s to %s", {file_id}, color)
        return True
    except FileNotFoundError as fnf_e:
        if not os.path.isfile(os.path.join(DATA_DONE, color, file_id)):
            logger.error(str(fnf_e))
            return False
        logger.info("image %s already at %s", file_id, color)
        return True


def process_msg(msg: str) -> None:
    if msg is None:
        return

    rgba, file_id, session_id = get_message_data(msg)
    file_path = os.path.join(DATA_PROCESS, f"{file_id}_{session_id}")
    if not is_valid_input_file(file_path, REDIS_HOST, REDIS_PORT, FAILOVER_Q):
        return

    if not file_id or not session_id or not rgba:
        logger.error("bad message received msg %s", msg)
        remove_msg(REDIS_HOST, REDIS_PORT, FAILOVER_Q)
        return

    color = get_colour_name(rgba)
    move_file_to_color(file_path, color, file_id)
    remove_msg(REDIS_HOST, REDIS_PORT, FAILOVER_Q)


def process_messages(host: str, port: int) -> None:
    process_msg(read_messages(host, port, INPUT_Q, FAILOVER_Q))
    process_msg(read_messages_failover(host, port, FAILOVER_Q))


async def listen() -> None:  # pragma: no cover
    while True:
        process_messages(REDIS_HOST, REDIS_PORT)
        await asyncio.sleep(0.1)
