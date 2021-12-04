import webcolors


def get_colour_name(rgb_triplet: list) -> str:
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        r_d = (r_c - rgb_triplet[0]) ** 2
        g_d = (g_c - rgb_triplet[1]) ** 2
        b_d = (b_c - rgb_triplet[2]) ** 2
        min_colours[(r_d + g_d + b_d)] = name
    return min_colours[min(min_colours.keys())]
