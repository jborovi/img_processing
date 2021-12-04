import os
import typing

import numpy as np
from PIL import Image


def get_image_rgba(
    path: typing.Union[str, bytes, os.PathLike], alpha_value_threshold: int
) -> np.ndarray:
    arr = np.array(Image.open(path).convert("RGBA"))
    return remove_transparent_pixels(arr, alpha_value_threshold)


def remove_transparent_pixels(arr: np.ndarray, rgba_alpha_threshold: int) -> np.ndarray:
    # deleting transparent pixels
    # with less alpha than transpancy rgba_alpha_threshold
    # as pixels with tranparent alpha == 0
    # changes the rgba mean of the whole image
    # even if the pixels are not visible
    arr = arr.flatten()
    arr = np.reshape(arr, (int(arr.shape[0] / 4), 4))
    arr = arr[np.where(arr[:, 3] >= rgba_alpha_threshold)]
    return arr


def get_image_rgba_mean(
    path: typing.Union[str, bytes, os.PathLike], rgba_alpha_threshold: int
) -> np.ndarray:
    return np.mean(get_image_rgba(path, rgba_alpha_threshold), axis=0)
