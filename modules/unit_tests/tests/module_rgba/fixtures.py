import os
import shutil

import pytest
import redis

from ..common import DIR_DEFAULT_VOLUME_PROCESS
from .common_module_rgba import REDIS_HOST, REDIS_PORT


@pytest.fixture(name="setup_module_rgba")
def setup_m_rgba(clean_module_rgba):  # pylint: disable=unused-argument
    os.makedirs(DIR_DEFAULT_VOLUME_PROCESS)


@pytest.fixture(name="clean_module_rgba")
def clean_m_rgba():
    conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    conn.flushdb()
    try:
        shutil.rmtree(DIR_DEFAULT_VOLUME_PROCESS)
    except FileNotFoundError:
        pass
