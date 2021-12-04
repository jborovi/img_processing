import os

import pytest
from module_input.utils_file import files_in_path, get_digest

from .fixtures import DIR_DATA_EMPTY, DIR_DATA_OK, FILE_OK

NUM_OK_FILES = 10


def test_utils_file_output_ok(setup_ok):  # pylint: disable=unused-argument
    res_test = list(files_in_path(DIR_DATA_OK))
    assert len(res_test) == NUM_OK_FILES
    expected_res = [f"{i}_{FILE_OK}" for i in range(0, NUM_OK_FILES)]
    assert sorted(res_test) == sorted(expected_res)


def test_utils_file_output_empty(empty_dir):  # pylint: disable=unused-argument
    res_test = list(files_in_path(DIR_DATA_EMPTY))
    assert len(res_test) == 0
    expected_res = []
    assert sorted(res_test) == sorted(expected_res)


def test_utils_file_not_existing_path(setup_ok):  # pylint: disable=unused-argument
    res = list(files_in_path("/NOTEXISTING"))
    assert res == []


def test_utils_file_sha(setup_ok):  # pylint: disable=unused-argument
    expected_res = "f3e7d8a947c3f443aea3b6f533e0048a89d08bb2e48901b0a88514db10c4d6a7"
    assert expected_res == get_digest(os.path.join(DIR_DATA_OK, f"{0}_{FILE_OK}"))


def test_utils_file_sha_not_found_error(setup_ok):  # pylint: disable=unused-argument
    with pytest.raises(FileNotFoundError):
        get_digest(os.path.join("/NOTEXISTING", f"{0}_{FILE_OK}"))
