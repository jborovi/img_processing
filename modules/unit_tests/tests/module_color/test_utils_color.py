from module_color import utils_color


def test_get_colour_name():
    res = utils_color.get_colour_name([255, 255, 255, 0])
    assert res == "white"
