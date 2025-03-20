from os import listdir
from template_tool import path
from template_tool.colorization import color
from colorama import init, Fore

init(convert=True)
def list():
    templates = listdir(path)
    for i in templates:
        print(color(Fore.GREEN,i ))
