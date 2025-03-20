from os.path import join, exists
from os import mkdir

if not exists(join("C:\\", "Templates")):
    mkdir(join("C:\\", "Templates"))
path = "C:\\Templates"
args_desc = {
    "--load": "load a template",
    "--save": "save a template",
    "--list": "list your templates",
    "--remove": "remove a template"
}

__all__ = ["path", "args_desc"]
