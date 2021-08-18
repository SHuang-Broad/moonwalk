#!/usr/bin/env python3

import json
import pandas as pd

from json2html import *

root_dir = "../"

table_center = "class=\"equalDivide\" style=\"border:3px solid black;margin-left:auto;margin-right:auto;font-size:70%\""

workflow_name = 'PBFlowcell.'


def __organize_input_json(json_loads) -> dict:
    input_names = [e[0].split('.') for e in json_loads]
    input_types = [e[1] for e in json_loads]
    level = [len(i)-2 for i in input_names]
    df = pd.DataFrame({'input_name': input_names, 'input_type': input_types, 'level': level})

    root = df[df['level'] == 0].copy().reset_index()
    root['n'] = root['input_name'].apply(lambda l: '.'.join(l))
    root = root.iloc[root['n'].apply(lambda s: len(s)).sort_values().index]

    others = df[df['level'] > 0].copy().reset_index()
    others['n'] = others['input_name'].apply(lambda l: '.'.join(l))
    others.sort_values(by=['level', 'n'], kind='stable', inplace=True)
    sorted_df = pd.concat([root, others], ignore_index=True)
    ready = sorted_df.set_index('n', drop=True).drop(labels=['level', 'index', 'input_name'], axis=1)
    return ready['input_type'].to_dict()


def format_2_html(json_file: str,
                  prefix_to_rm: str,
                  is_input: bool) -> None:

    with open(json_file) as json_file:
        json_contents = json.load(json_file)
    ll = json.loads(json.dumps(sorted(json_contents.items()), sort_keys=True))
    if is_input:
        sorted_by_keys = __organize_input_json(ll)
    else:
        sorted_by_keys = dict((e[0], e[1]) for e in ll)

    raw = json2html.convert(json=sorted_by_keys, table_attributes=table_center)
    formatted = raw.replace('<th>', '<th align=\"left\">').replace(prefix_to_rm, '')
    return formatted


if __name__ == "__main__":

    output_path = f'{root_dir}precompiled_htmls/wdl_io.html'
    front_matter = (
        f"---\n"
        f"layout: plain_two_columns\n"
        f"---\n"
    )
    with open(output_path, 'w') as html_file:
        html_file.write(front_matter)
        html_file.write("<div class=\"row\">\n")

        html_file.write("<div class=\"column\">\n")
        html_file.write("<h1>Inputs</h1>")
        html_file.write(format_2_html(f'{root_dir}_data/wdl_inputs.json', workflow_name, True))
        html_file.write("\n")
        html_file.write("</div>\n")

        html_file.write("<div class=\"column\">\n")
        html_file.write("<h1>Outputs</h1>")
        html_file.write(format_2_html(f'{root_dir}_data/wdl_outputs.json', workflow_name, False))
        html_file.write("\n")
        html_file.write("</div>\n")

        html_file.write("</div>\n")
