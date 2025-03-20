from tkinter.filedialog import askopenfilenames
from os import mkdir, _exit
from os.path import (
    join,
    exists,
    basename,
)
from shutil import copy
from template_tool import path
from json import dump


def save(name: str | None = None):
    files = askopenfilenames(filetypes=[("python files", "*.py")])

    if exists(join(path, name)):
        print("template already exists")
        _exit(1)
    else:
        mkdir(join(path, name))

    listfiles = []

    for i in files:
        copy(i, join(path, name, basename(i)))
        listfiles.append(basename(i))

    with open(join(path, name, "template.json"), "w") as f:
        dump({"Files": listfiles}, f)
