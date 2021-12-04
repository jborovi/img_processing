import json
import os
import shutil
import uuid

import redis
from img_processing_common.messaging import read_messages, send_message
from module_color import event_listener

from ..common import (DIR_DEFAULT_VOLUME_DONE, DIR_DEFAULT_VOLUME_PROCESS,
                      REDIS_HOST, REDIS_PORT)
from .common_module_color import (DIR_TEST_DATA, FILE_BAD, FILE_OK,
                                  check_redis_rgba_q_is_empty)


def test_run_with_redis(
    setup_module_color, monkeypatch
):  # pylint: disable=unused-argument
    test_file_sha = "d13aee4e4b349411e4ff7c84af8870e7dcb8163e8b9f6500d5f3683bd0af2ce5"
    session_id = str(uuid.uuid4())
    msg = json.dumps(
        {
            "file_id": test_file_sha,
            "session_id": session_id,
            "rgba": [255.0, 255.0, 0.0, 255.0],
        }
    ).encode()

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
    msg_failover = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0).lpop(
        event_listener.FAILOVER_Q
    )

    assert msg_in is None
    assert msg_failover is None
    assert os.path.isfile(
        os.path.join(DIR_DEFAULT_VOLUME_DONE, "yellow", f"{test_file_sha}")
    )


def test_run_no_redis(setup_module_color):  # pylint: disable=unused-argument
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
    setup_module_color, monkeypatch
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
    assert msg_in is None
    assert msg_failover is None


def test_run_file_missing(setup_module_color):  # pylint: disable=unused-argument
    test_file_sha = "d13aee4e4b349411e4ff7c84af8870e7dcb8163e8b9f6500d5f3683bd0af2ce5"
    session_id = str(uuid.uuid4())

    msg = json.dumps({"file_id": test_file_sha, "session_id": session_id}).encode()
    assert os.path.isdir(DIR_DEFAULT_VOLUME_PROCESS)
    event_listener.process_msg(msg)
    check_redis_rgba_q_is_empty()


def test_none_message(setup_module_color):  # pylint: disable=unused-argument
    event_listener.process_msg(None)
    check_redis_rgba_q_is_empty()


def test_malformed_message(setup_module_color):  # pylint: disable=unused-argument
    event_listener.process_msg(json.dumps({}).encode())
    check_redis_rgba_q_is_empty()


def test_process_message_no_redis(
    setup_module_color, monkeypatch
):  # pylint: disable=unused-argument
    test_file_sha = "d13aee4e4b349411e4ff7c84af8870e7dcb8163e8b9f6500d5f3683bd0af2ce5"
    session_id = str(uuid.uuid4())
    msg = json.dumps(
        {
            "file_id": test_file_sha,
            "session_id": session_id,
            "rgba": [255.0, 255.0, 0.0, 255.0],
        }
    ).encode()

    monkeypatch.setattr(event_listener, "REDIS_HOST", "notexistinghost")
    shutil.copy(
        os.path.join(DIR_TEST_DATA, FILE_OK),
        os.path.join(DIR_DEFAULT_VOLUME_PROCESS, f"{test_file_sha}_{session_id}"),
    )
    send_message(REDIS_HOST, REDIS_PORT, event_listener.INPUT_Q, msg)

    event_listener.process_messages("NotExistingHost", REDIS_PORT)
    assert os.path.isfile(
        os.path.join(
            DIR_DEFAULT_VOLUME_PROCESS,
            f"{test_file_sha}_{session_id}",
        )
    )


def test_move_file_to_color(setup_module_color):  # pylint: disable=unused-argument
    test_file_sha = "d13aee4e4b349411e4ff7c84af8870e7dcb8163e8b9f6500d5f3683bd0af2ce5"
    session_id = str(uuid.uuid4())
    file_name = f"{test_file_sha}_{session_id}"
    file_path = os.path.join(DIR_DEFAULT_VOLUME_PROCESS, file_name)
    shutil.copy(
        os.path.join(DIR_TEST_DATA, FILE_OK),
        file_path,
    )
    assert event_listener.move_file_to_color(file_path, "yellow", test_file_sha)
    assert not os.path.isfile(file_path)
    assert os.path.isfile(
        os.path.join(DIR_DEFAULT_VOLUME_DONE, "yellow", test_file_sha)
    )


def test_move_file_to_color_file_missing(
    setup_module_color,
):  # pylint: disable=unused-argument
    test_file_sha = "d13aee4e4b349411e4ff7c84af8870e7dcb8163e8b9f6500d5f3683bd0af2ce5"
    session_id = str(uuid.uuid4())
    file_name = f"{test_file_sha}_{session_id}"
    file_path = os.path.join(DIR_DEFAULT_VOLUME_PROCESS, file_name)
    assert not event_listener.move_file_to_color(file_path, "yellow", file_name)
    assert not os.path.isfile(
        os.path.join(DIR_DEFAULT_VOLUME_DONE, "yellow", test_file_sha)
    )


def test_move_file_to_color_file_missing_already_in_color(
    setup_module_color,
):  # pylint: disable=unused-argument
    test_file_sha = "d13aee4e4b349411e4ff7c84af8870e7dcb8163e8b9f6500d5f3683bd0af2ce5"
    session_id = str(uuid.uuid4())
    file_name = f"{test_file_sha}_{session_id}"
    file_path = os.path.join(DIR_DEFAULT_VOLUME_PROCESS, file_name)
    os.makedirs(os.path.join(DIR_DEFAULT_VOLUME_DONE, "yellow"), exist_ok=True)
    shutil.copy(
        os.path.join(DIR_TEST_DATA, FILE_OK),
        os.path.join(DIR_DEFAULT_VOLUME_DONE, "yellow", test_file_sha),
    )
    assert os.path.isfile(
        os.path.join(DIR_DEFAULT_VOLUME_DONE, "yellow", test_file_sha)
    )

    assert event_listener.move_file_to_color(file_path, "yellow", test_file_sha)
    assert os.path.isfile(
        os.path.join(DIR_DEFAULT_VOLUME_DONE, "yellow", test_file_sha)
    )
    assert not os.path.isfile(os.path.join(DIR_DEFAULT_VOLUME_PROCESS, file_name))
