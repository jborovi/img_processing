import os
import shutil

import pytest
import redis

from ..common import (DIR_DEFAULT_VOLUME_DONE, DIR_DEFAULT_VOLUME_PROCESS,
                      REDIS_HOST, REDIS_PORT)


@pytest.fixture(name="setup_module_color")
def setup_m_color(clean_module_color):  # pylint: disable=unused-argument
    os.makedirs(DIR_DEFAULT_VOLUME_DONE)
    os.makedirs(DIR_DEFAULT_VOLUME_PROCESS)


@pytest.fixture(name="clean_module_color")
def clean_m_color():
    conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    conn.flushdb()
    try:
        shutil.rmtree(DIR_DEFAULT_VOLUME_DONE)
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree(DIR_DEFAULT_VOLUME_PROCESS)
    except FileNotFoundError:
        pass
