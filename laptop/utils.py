# -*- coding: utf-8 -*-

import typing as T

from .vendor.pathlib_mate import Path


def add_line(p: Path, line: str):
    lines = p.read_text().split("\n")
    if line in lines:
        return
    else:
        lines.append(line)
        p.write_text("\n".join(lines) + "\n")
