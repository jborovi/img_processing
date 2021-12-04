import os

import numpy as np
from module_rgba.utils_img import get_image_rgba, get_image_rgba_mean

from .common_module_rgba import DIR_TEST_DATA


def test_image_rgba_remove_transparent(
    clean_module_rgba,
):  # pylint: disable=unused-argument
    res = get_image_rgba(os.path.join(DIR_TEST_DATA, "yellowtransparent.png"), 128)
    assert np.all(
        res == np.array([255, 255, 0, 255])
    ), f"all pixels should be {[255, 255, 0, 255]}"


def test_image_rgba_keep_transparent(
    clean_module_rgba,
):  # pylint: disable=unused-argument
    res = get_image_rgba(os.path.join(DIR_TEST_DATA, "yellowtransparent.png"), -1)

    assert np.any(
        res != np.array([255, 255, 0, 255])
    ), "there should be some extra transparent pixels"


def test_get_image_rgba_mean(clean_module_rgba):  # pylint: disable=unused-argument
    res = get_image_rgba_mean(
        (os.path.join(DIR_TEST_DATA, "yellowtransparent.png")), 128
    )
    assert res.shape == (4,)
    assert np.all(res == np.array([255, 255, 0, 255]))
