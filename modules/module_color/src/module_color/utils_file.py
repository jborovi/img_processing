import os

from img_processing_common.conf import DATA_DONE


def create_path_color(color: str) -> None:
    color_path = os.path.join(DATA_DONE, color)
    os.makedirs(color_path, exist_ok=True)
    return color_path
