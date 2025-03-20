from os import system as bat
from os.path import join, exists
from template_tool import path

def remove(template:str | None=None):
    if exists(join(path, template)):
        bat(f"rd /s /q \"{join(path, template)}\"")

