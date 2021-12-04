import redis
from module_color import event_listener

from ..common import REDIS_HOST, REDIS_PORT

DIR_TEST_DATA = "/tests/test_data/module_rgba"

FILE_OK = "yellowtransparent.png"
FILE_BAD = "noimage.txt"


def check_redis_rgba_q_is_empty():
    assert (
        redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0).lpop(event_listener.INPUT_Q)
        is None
    )
    assert (
        redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0).lpop(
            event_listener.FAILOVER_Q
        )
        is None
    )
