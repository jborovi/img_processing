import os

from module_color import utils_file

from ..common import DIR_DEFAULT_VOLUME_DONE


def test_utils_file(setup_module_color):  # pylint: disable=unused-argument
    utils_file.create_path_color("black")
    assert os.path.exists(os.path.join(DIR_DEFAULT_VOLUME_DONE, "black"))


def test_utils_file_already_exists(
    setup_module_color,
):  # pylint: disable=unused-argument
    utils_file.create_path_color("black")
    utils_file.create_path_color("black")
    assert os.path.exists(os.path.join(DIR_DEFAULT_VOLUME_DONE, "black"))
