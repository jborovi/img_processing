"""
main logic of module
reads messages from INPUT_Q
reads file from DATA_PROCESS and gets information about average rgba
then sends rgba to OUTPUT_Q
messages are read from FAILOVER_Q once
if received file is not valid picture, it gets deleted
"""

import asyncio
import json
import os

import redis
from img_processing_common.conf import DATA_PROCESS
from img_processing_common.logger import logger
from img_processing_common.messaging import (read_messages,
                                             read_messages_failover,
                                             remove_msg, send_message)
from img_processing_common.utils_img import is_valid_input_file

from .utils_img import get_image_rgba_mean

INPUT_Q = os.getenv("INPUT_Q_MODULE_RGBA", "module_rgba")
OUTPUT_Q = os.getenv("INPUT_Q_MODULE_COLOR", "module_color")
FAILOVER_Q = f"processing_rgba_{os.getenv('WORKER_ID', 'unknown')}"

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


def get_msg_data(msg: str) -> tuple:
    file_id = json.loads(msg.decode()).get("file_id")
    session_id = json.loads(msg.decode()).get("session_id")
    file_path = os.path.join(DATA_PROCESS, f"{file_id}_{session_id}")
    return (file_id, session_id, file_path)


def process_msg(msg: str) -> None:
    if msg is None:
        return
    file_id, session_id, file_path = get_msg_data(msg)
    if not is_valid_input_file(file_path, REDIS_HOST, REDIS_PORT, FAILOVER_Q):
        return

    if not file_id or not session_id:
        logger.error("bad message received msg %s", msg)
        remove_msg(REDIS_HOST, REDIS_PORT, FAILOVER_Q)
        return

    try:
        rgba_mean = get_image_rgba_mean(
            os.path.join(DATA_PROCESS, f"{file_id}_{session_id}"),
            128,
        )
        msg = json.dumps(
            {"file_id": file_id, "session_id": session_id, "rgba": rgba_mean.tolist()}
        ).encode()
        send_message(REDIS_HOST, REDIS_PORT, OUTPUT_Q, msg)
    except FileNotFoundError as fnf_e:
        logger.error(str(fnf_e))
    except redis.exceptions.ConnectionError:
        return

    remove_msg(REDIS_HOST, REDIS_PORT, FAILOVER_Q)


def process_messages(host: str, port: int) -> None:
    process_msg(read_messages(host, port, INPUT_Q, FAILOVER_Q))
    process_msg(read_messages_failover(host, port, FAILOVER_Q))


async def listen() -> None:  # pragma: no cover
    while True:
        process_messages(REDIS_HOST, REDIS_PORT)
        await asyncio.sleep(0.1)
