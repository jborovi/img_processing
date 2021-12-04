import os
import shutil

import pytest
import redis

from ..common import DIR_DEFAULT_VOLUME, REDIS_HOST, REDIS_PORT
from .common_module_input import (DIR_DATA_EMPTY, DIR_DATA_OK, DIR_TEST_DATA,
                                  FILE_OK)


@pytest.fixture(name="setup_ok")
def ok_setup(clean_module_input):  # pylint: disable=unused-argument
    os.mkdir(DIR_DATA_OK)
    for i in range(0, 10):
        file_out = os.path.join(DIR_DATA_OK, f"{i}_{FILE_OK}")
        shutil.copy(os.path.join(DIR_TEST_DATA, FILE_OK), file_out)


@pytest.fixture(name="empty_dir")
def setup_empty_dir(clean_module_input):  # pylint: disable=unused-argument
    os.mkdir(DIR_DATA_EMPTY)


@pytest.fixture(name="clean_module_input")
def clean_m_input():
    conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    conn.flushdb()
    try:
        shutil.rmtree(DIR_DEFAULT_VOLUME)
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree(DIR_DATA_OK)
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree(DIR_DATA_EMPTY)
    except FileNotFoundError:
        pass
