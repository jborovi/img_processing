import json
import os
import shutil
import uuid

import redis
from module_input import input_process, utils_file

from ..common import (DIR_DEFAULT_VOLUME_INPUT, DIR_DEFAULT_VOLUME_PROCESS,
                      REDIS_HOST, REDIS_PORT)
from .common_module_input import DIR_TEST_DATA, FILE_NOT_IMAGE, FILE_OK

DIR_INPUT = "/tmp/images/input"
DIR_PROCESS = "/tmp/images/process"


def test_setup_empty(clean_module_input):  # pylint: disable=unused-argument
    input_process.setup()
    assert os.path.isdir(DIR_INPUT)
    assert os.path.isdir(DIR_PROCESS)


def test_setup_dirs_exists(clean_module_input):  # pylint: disable=unused-argument
    os.makedirs(DIR_INPUT)
    os.makedirs(DIR_PROCESS)
    input_process.setup()
    assert os.path.isdir(DIR_INPUT)
    assert os.path.isdir(DIR_PROCESS)


def test_run_no_valid_image(clean_module_input):  # pylint: disable=unused-argument
    input_process.setup()
    shutil.copy(
        os.path.join(DIR_TEST_DATA, FILE_NOT_IMAGE),
        os.path.join(DIR_DEFAULT_VOLUME_INPUT, FILE_NOT_IMAGE),
    )
    input_process.process_inputs(DIR_DEFAULT_VOLUME_INPUT)
    assert os.path.isdir(DIR_INPUT)
    assert os.path.isdir(DIR_PROCESS)
    assert [] == list(utils_file.files_in_path(DIR_DEFAULT_VOLUME_INPUT))


def test_run_not_existing_file_id(
    clean_module_input, monkeypatch
):  # pylint: disable=unused-argument
    monkeypatch.setattr(
        input_process,
        "files_in_path",
        lambda x: [
            "notexisting",
        ],
    )
    input_process.setup()
    input_process.process_inputs(DIR_DEFAULT_VOLUME_INPUT)
    assert os.path.isdir(DIR_INPUT)
    assert os.path.isdir(DIR_PROCESS)
    assert True, "OK, no exception thrown"


def test_run_no_redis(clean_module_input):  # pylint: disable=unused-argument
    expected_fname_part = (
        "f3e7d8a947c3f443aea3b6f533e0048a89d08bb2e48901b0a88514db10c4d6a7"
    )
    input_process.setup()
    shutil.copy(
        os.path.join(DIR_TEST_DATA, FILE_OK),
        os.path.join(DIR_DEFAULT_VOLUME_INPUT, FILE_OK),
    )
    input_process.process_inputs(DIR_DEFAULT_VOLUME_INPUT)
    assert os.path.isdir(DIR_INPUT)
    assert os.path.isdir(DIR_PROCESS)
    assert (
        expected_fname_part
        == list(utils_file.files_in_path(DIR_DEFAULT_VOLUME_INPUT))[0]
    )


def test_run_with_redis(
    clean_module_input, monkeypatch
):  # pylint: disable=unused-argument
    expected_fname_part = (
        "f3e7d8a947c3f443aea3b6f533e0048a89d08bb2e48901b0a88514db10c4d6a7"
    )
    monkeypatch.setattr(input_process, "REDIS_HOST", REDIS_HOST)
    monkeypatch.setattr(input_process, "REDIS_PORT", REDIS_PORT)
    input_process.setup()
    shutil.copy(
        os.path.join(DIR_TEST_DATA, FILE_OK),
        os.path.join(DIR_DEFAULT_VOLUME_INPUT, FILE_OK),
    )
    input_process.process_inputs(DIR_DEFAULT_VOLUME_INPUT)
    assert os.path.isdir(DIR_INPUT)
    assert os.path.isdir(DIR_PROCESS)

    filename_parts = list(utils_file.files_in_path(DIR_DEFAULT_VOLUME_PROCESS))[
        0
    ].split("_")
    msg = json.loads(
        redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        .lpop(input_process.OUTPUT_Q)
        .decode()
    )
    assert msg.get("file_id") == expected_fname_part
    assert filename_parts[0] == expected_fname_part
    try:
        uuid.UUID(str(filename_parts[1]))
        uuid.UUID(msg.get("session_id"))
        assert True
    except ValueError:
        assert False, "filename part is not uuid"
