"""
Functions to communicate with MQ broker
"""

import redis

from .logger import logger


def send_message(host: str, port: int, queue: str, msg: str) -> None:
    try:
        redis.Redis(host=host, port=port, db=0).lpush(queue, msg)
        logger.info("sent to %s msg %s", queue, msg)
    except redis.exceptions.ConnectionError as conn_e:
        logger.error(str(conn_e))
        raise conn_e


def read_messages(host: str, port: int, queue: str, failover_q: str) -> str:
    try:
        return redis.Redis(host=host, port=port, db=0).rpoplpush(queue, failover_q)
    except redis.exceptions.ConnectionError as conn_e:
        logger.error(str(conn_e))
        return None


def remove_msg(host: str, port: int, queue: str):
    try:
        logger.info("removing failover msg from queue %s", queue)
        return redis.Redis(host=host, port=port, db=0).lpop(queue)
    except redis.exceptions.ConnectionError as conn_e:
        logger.error(str(conn_e))
        return None


def read_messages_failover(host: str, port: int, queue: str) -> str:
    try:
        return redis.Redis(host=host, port=port, db=0).lpop(queue)
    except redis.exceptions.ConnectionError as conn_e:
        logger.error(str(conn_e))
        return None
