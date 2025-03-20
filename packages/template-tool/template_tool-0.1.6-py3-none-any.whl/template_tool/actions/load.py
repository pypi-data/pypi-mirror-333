from os.path import (
    join,
    exists,
)
from os import (
    _exit,
    mkdir,
    system as bat,
)
from shutil import copy
from json import load as loadjson
from template_tool import path


def load(name: str | None = None) -> None:
    if not exists(join(path, name) or not exists(join(path, name, "template.json"))):
        print("Template Not Exist")
        _exit(1)
    with open(join(path, name, "template.json"), "r") as f:
        template = loadjson(f)
        if "Files" not in template.keys():
            print("Template Not Exist")
            _exit(1)
        f.close()

    if exists(name):
        if input("There is a folder with the same name, would you replace it with the template? (Y, N)").upper() == "Y":
            bat(f"rd /s /q {name}")
        else:
            _exit(1)

    mkdir(name)
    for i in template["Files"]:
        if i.endswith(".py"):
            copy(join(path, name, i), join(name, i))
