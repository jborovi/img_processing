import json
import os
import shutil
import uuid

import numpy as np
import redis
from img_processing_common.messaging import read_messages, send_message
from module_rgba import event_listener

from ..common import DIR_DEFAULT_VOLUME_PROCESS, REDIS_HOST, REDIS_PORT
from .common_module_rgba import (DIR_TEST_DATA, FILE_BAD, FILE_OK,
                                 check_redis_rgba_q_is_empty, is_valid_uuid)


def test_run_with_redis(
    setup_module_rgba, monkeypatch
):  # pylint: disable=unused-argument
    test_file_sha = "d13aee4e4b349411e4ff7c84af8870e7dcb8163e8b9f6500d5f3683bd0af2ce5"
    session_id = str(uuid.uuid4())
    msg = json.dumps({"file_id": test_file_sha, "session_id": session_id}).encode()

    monkeypatch.setattr(event_listener, "REDIS_HOST", REDIS_HOST)
    monkeypatch.setattr(event_listener, "REDIS_PORT", REDIS_PORT)
    shutil.copy(
        os.path.join(DIR_TEST_DATA, FILE_OK),
        os.path.join(DIR_DEFAULT_VOLUME_PROCESS, f"{test_file_sha}_{session_id}"),
    )
    send_message(REDIS_HOST, REDIS_PORT, event_listener.INPUT_Q, msg)

    event_listener.process_messages(REDIS_HOST, REDIS_PORT)

    msg_in = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0).lpop(
        event_listener.INPUT_Q
    )
    msg_out = json.loads(
        redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        .lpop(event_listener.OUTPUT_Q)
        .decode()
    )
    msg_failover = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0).lpop(
        event_listener.FAILOVER_Q
    )

    assert msg_in is None
    assert msg_failover is None
    assert (
        msg_out.get("file_id")
        == "d13aee4e4b349411e4ff7c84af8870e7dcb8163e8b9f6500d5f3683bd0af2ce5"
    )
    assert is_valid_uuid(msg_out.get("session_id"))
    assert np.all(msg_out.get("rgba") == np.array([255, 255, 0, 255]))
    assert os.path.isfile(
        os.path.join(
            DIR_DEFAULT_VOLUME_PROCESS,
            f"{test_file_sha}_{session_id}",
        )
    )


def test_run_no_redis(setup_module_rgba):  # pylint: disable=unused-argument
    test_file_sha = "d13aee4e4b349411e4ff7c84af8870e7dcb8163e8b9f6500d5f3683bd0af2ce5"
    session_id = str(uuid.uuid4())

    assert os.path.isdir(DIR_DEFAULT_VOLUME_PROCESS)
    shutil.copy(
        os.path.join(DIR_TEST_DATA, FILE_OK),
        os.path.join(DIR_DEFAULT_VOLUME_PROCESS, f"{test_file_sha}_{session_id}"),
    )
    event_listener.process_msg(
        read_messages(
            "notexistingHOST", 6379, event_listener.INPUT_Q, event_listener.FAILOVER_Q
        )
    )
    assert os.path.isfile(
        os.path.join(
            DIR_DEFAULT_VOLUME_PROCESS,
            f"{test_file_sha}_{session_id}",
        )
    )


def test_run_with_redis_bad_file(
    setup_module_rgba, monkeypatch
):  # pylint: disable=unused-argument
    test_file_sha = "d13aee4e4b349411e4ff7c84af8870e7dcb8163e8b9f6500d5f3683bd0af2ce5"
    session_id = str(uuid.uuid4())

    msg = json.dumps({"file_id": test_file_sha, "session_id": session_id}).encode()
    monkeypatch.setattr(event_listener, "REDIS_HOST", REDIS_HOST)
    monkeypatch.setattr(event_listener, "REDIS_PORT", REDIS_PORT)
    assert os.path.isdir(DIR_DEFAULT_VOLUME_PROCESS)
    shutil.copy(
        os.path.join(DIR_TEST_DATA, FILE_BAD),
        os.path.join(DIR_DEFAULT_VOLUME_PROCESS, f"{test_file_sha}_{session_id}"),
    )
    event_listener.process_msg(msg)
    assert not os.path.isfile(
        os.path.join(
            DIR_DEFAULT_VOLUME_PROCESS,
            f"{test_file_sha}_{session_id}",
        )
    )
    msg_in = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0).lpop(
        event_listener.INPUT_Q
    )
    msg_failover = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0).lpop(
        event_listener.FAILOVER_Q
    )
    msg_out = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0).lpop(
        event_listener.OUTPUT_Q
    )
    assert msg_in is None
    assert msg_out is None
    assert msg_failover is None


def test_run_file_missing(setup_module_rgba):  # pylint: disable=unused-argument
    test_file_sha = "d13aee4e4b349411e4ff7c84af8870e7dcb8163e8b9f6500d5f3683bd0af2ce5"
    session_id = str(uuid.uuid4())

    msg = json.dumps({"file_id": test_file_sha, "session_id": session_id}).encode()
    assert os.path.isdir(DIR_DEFAULT_VOLUME_PROCESS)
    event_listener.process_msg(msg)
    check_redis_rgba_q_is_empty()


def test_none_message(setup_module_rgba):  # pylint: disable=unused-argument
    event_listener.process_msg(None)
    check_redis_rgba_q_is_empty()


def test_malformed_message(setup_module_rgba):  # pylint: disable=unused-argument
    event_listener.process_msg(json.dumps({}).encode())
    check_redis_rgba_q_is_empty()


def test_process_message_no_redis(
    setup_module_rgba, monkeypatch
):  # pylint: disable=unused-argument
    test_file_sha = "d13aee4e4b349411e4ff7c84af8870e7dcb8163e8b9f6500d5f3683bd0af2ce5"
    session_id = str(uuid.uuid4())
    msg = json.dumps({"file_id": test_file_sha, "session_id": session_id}).encode()

    monkeypatch.setattr(event_listener, "REDIS_HOST", "notexistinghost")
    shutil.copy(
        os.path.join(DIR_TEST_DATA, FILE_OK),
        os.path.join(DIR_DEFAULT_VOLUME_PROCESS, f"{test_file_sha}_{session_id}"),
    )
    send_message(REDIS_HOST, REDIS_PORT, event_listener.INPUT_Q, msg)

    event_listener.process_msg(msg)
    assert os.path.isfile(
        os.path.join(
            DIR_DEFAULT_VOLUME_PROCESS,
            f"{test_file_sha}_{session_id}",
        )
    )
