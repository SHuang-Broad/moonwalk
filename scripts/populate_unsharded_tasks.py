#!/usr/bin/env python3

import json
import os.path

from json2html import *


from os import listdir
from os.path import isfile, join


root_dir = "../"
images_dir_under_root = "assets/images"
images_dir = f"{root_dir}{images_dir_under_root}"
images_extension = ".svg"




def __output_one_figure(svg_base_name: str):
    return f"    <img src=\"/{images_dir_under_root}/{os.path.basename(svg_base_name)}\" style=\"width:400px;height:400px;\">\n"


def __output_a_column(svg_base_name_1: str, svg_base_name_2: str):
    html = "\n  <div class=\"column\">\n"
    html += __output_one_figure(svg_base_name_1)
    html += __output_one_figure(svg_base_name_2)
    html += "  </div>\n"
    return html


if __name__ == "__main__":

    only_files = [join(images_dir, f) for f in listdir(images_dir) if isfile(join(images_dir, f))]
    only_images = [f for f in only_files if f.endswith(images_extension)]

    output_path = f'{root_dir}precompiled_htmls/unsharded_tasks.html'
    front_matter = (
        f"---\n"
        f"layout: unsharded_tasks\n"
        f"---\n"
    )
    with open(output_path, 'w') as html_file:
        html_file.write(front_matter)
        html_file.write("\n")
        html_file.write("<div class=\"row\">")

        for i in range(0, len(only_images), 2):
            # print(os.path.basename(only_images[i]))
            s = __output_a_column(only_images[i], only_images[i+1])
            html_file.write(s)

    # with open(output_path, 'a') as html_file:
        html_file.write("\n")
        html_file.write("</div>")