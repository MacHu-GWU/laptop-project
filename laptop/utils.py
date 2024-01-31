# -*- coding: utf-8 -*-

import typing as T

from .vendor.pathlib_mate import Path


def add_line(p: Path, line: T.Union[str, T.List[str]]):
    lines = p.read_text().split("\n")
    flag = False
    if isinstance(line, str):
        line_list = [line]
    else:
        line_list = line
    print(lines)
    for line in line_list:
        if line not in lines:
            lines.append(line)
            flag = True
    if flag:
        p.write_text("\n".join(lines) + "\n")
