# -*- coding: UTF-8 -*-
import os


def del_note(s):
    return s.split("#")[0].strip().strip('"').strip("'")


def get_pattern(config_filepath) -> str:
    release_short, release_version, release_type_suffix = "", "", ""
    if not os.path.isfile(config_filepath):
        return "no_config_file"

    for i in open(config_filepath, "r"):
        if i.strip() and i.find("release_short") >= 0 and not release_short:
            release_short = del_note(i.split("=")[-1].strip() or "")
        elif i.strip() and i.find("release_version") >= 0 and not release_version:
            release_version = del_note(i.split("=")[-1].strip() or "")
        elif i.strip() and i.find("release_type_suffix") >= 0 and not release_type_suffix:
            release_type_suffix = del_note(i.split("=")[-1].strip() or "")
    return "%s-%s%s" % (release_short, release_version, release_type_suffix)
